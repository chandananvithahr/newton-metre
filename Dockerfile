# ── Stage 1: Build dwg2dxf (static) + dwg2svg (dynamic) from LibreDWG ───────
FROM python:3.11-slim AS builder

# libxml2-dev required for dwg2svg SVG output
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make ca-certificates curl xz-utils pkg-config file \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -o /tmp/libredwg.tar.xz \
    https://github.com/LibreDWG/libredwg/releases/download/0.13.4/libredwg-0.13.4.tar.xz \
    && cd /tmp && tar xf libredwg.tar.xz

WORKDIR /tmp/libredwg-0.13.4

# Build dwg2dxf (static — no runtime deps needed)
RUN LDFLAGS="-static" CFLAGS="-O2" ./configure \
        --disable-shared --disable-python --disable-perl --enable-static \
    && make -j$(nproc) -C src \
    && make -j$(nproc) -C programs dwg2dxf \
    && cp programs/dwg2dxf /tmp/dwg2dxf \
    && chmod +x /tmp/dwg2dxf

# Build dwg2svg (reads DWG binary directly → SVG, bypasses ezdxf entirely)
# This is the Level 2 fallback for AutoCAD 2018+ DWGs with corrupt handles
# Always creates /tmp/dwg2svg so the COPY below never fails (empty = not available)
RUN (./configure --disable-python --disable-perl \
    && make -j$(nproc) -C src \
    && make -j$(nproc) -C programs dwg2SVG \
    && cp programs/dwg2SVG /tmp/dwg2svg \
    && chmod +x /tmp/dwg2svg \
    && echo "dwg2svg built OK") \
    || (echo "dwg2svg build failed — creating placeholder" && touch /tmp/dwg2svg)

# ── Stage 2: Production image ────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Runtime deps: libxml2 for dwg2svg, cairo+pango for cairosvg (SVG→PNG)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Copy dwg2dxf and dwg2svg from builder (dwg2svg may be an empty placeholder)
COPY --from=builder /tmp/dwg2dxf /usr/local/bin/dwg2dxf
COPY --from=builder /tmp/dwg2svg /usr/local/bin/dwg2svg

RUN chmod +x /usr/local/bin/dwg2dxf \
    && (dwg2dxf --help >/dev/null 2>&1 && echo "dwg2dxf OK" || echo "dwg2dxf binary present") \
    && ([ -s /usr/local/bin/dwg2svg ] && chmod +x /usr/local/bin/dwg2svg && echo "dwg2svg OK" \
        || (rm -f /usr/local/bin/dwg2svg && echo "dwg2svg not available — raw text fallback only"))

# Install Python dependencies (cached layers)
COPY costimize-v2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY costimize-v2/api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# cairosvg: converts SVG→PNG for the DWG vision fallback path
RUN pip install --no-cache-dir cairosvg

# Copy application code
COPY costimize-v2/api/ api/
COPY costimize-v2/agents/ agents/
COPY costimize-v2/engines/ engines/
COPY costimize-v2/extractors/ extractors/
COPY costimize-v2/scrapers/ scrapers/
COPY costimize-v2/history/ history/
COPY costimize-v2/config.py config.py
COPY costimize-v2/data/materials.json data/materials.json
COPY costimize-v2/data/processes.json data/processes.json

# Create writable data directories
RUN mkdir -p /app/data/validation /app/data/cache /app/data/similarity

ENV PYTHONPATH=/app

RUN adduser --disabled-password --no-create-home --gecos "" appuser \
    && chown -R appuser:appuser /app/data

USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
