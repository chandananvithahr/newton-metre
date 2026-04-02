# Stage 1: Build LibreDWG dwg2dxf binary
FROM python:3.11-slim AS dwg-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake gcc g++ make git ca-certificates \
    && git clone --depth 1 https://github.com/LibreDWG/libredwg.git /tmp/libredwg \
    && cd /tmp/libredwg && mkdir build && cd build \
    && cmake .. -DCMAKE_BUILD_TYPE=Release \
    && make -j$(nproc) dwg2dxf

# Stage 2: Production image
FROM python:3.11-slim

WORKDIR /app

# Copy dwg2dxf + libredwg shared lib from builder
COPY --from=dwg-builder /tmp/libredwg/build/programs/dwg2dxf /usr/local/bin/dwg2dxf
COPY --from=dwg-builder /tmp/libredwg/build/src/libredwg.so* /usr/local/lib/
RUN ldconfig

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

COPY . .

ENV PYTHONPATH=/app

RUN adduser --disabled-password --no-create-home --gecos "" appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
