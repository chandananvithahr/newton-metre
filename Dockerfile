# ── Stage 1: Build static dwg2dxf binary from LibreDWG ──────────────────────
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ make ca-certificates curl xz-utils pkg-config file \
    && rm -rf /var/lib/apt/lists/*

RUN curl -L -o /tmp/libredwg.tar.xz \
    https://github.com/LibreDWG/libredwg/releases/download/0.13.4/libredwg-0.13.4.tar.xz \
    && cd /tmp && tar xf libredwg.tar.xz

WORKDIR /tmp/libredwg-0.13.4
RUN LDFLAGS="-static" CFLAGS="-O2" ./configure \
        --disable-shared --disable-python --disable-perl --enable-static \
    && make -j$(nproc) -C src \
    && make -j$(nproc) -C programs dwg2dxf \
    && cp programs/dwg2dxf /tmp/dwg2dxf \
    && chmod +x /tmp/dwg2dxf

# ── Stage 2: Production image ────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy static dwg2dxf binary from builder
COPY --from=builder /tmp/dwg2dxf /usr/local/bin/dwg2dxf
RUN chmod +x /usr/local/bin/dwg2dxf && (dwg2dxf --help >/dev/null 2>&1 || echo "dwg2dxf binary present")

# Install Python dependencies (cached layers)
COPY costimize-v2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY costimize-v2/api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

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
