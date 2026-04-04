FROM python:3.11-slim

WORKDIR /app

COPY costimize-v2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY costimize-v2/api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copy only the code needed for the API (no papers/sandvik/docs)
COPY costimize-v2/api/ api/
COPY costimize-v2/agents/ agents/
COPY costimize-v2/engines/ engines/
COPY costimize-v2/extractors/ extractors/
COPY costimize-v2/scrapers/ scrapers/
COPY costimize-v2/history/ history/
COPY costimize-v2/config.py config.py
COPY costimize-v2/data/materials.json data/materials.json
COPY costimize-v2/data/processes.json data/processes.json

ENV PYTHONPATH=/app

RUN adduser --disabled-password --no-create-home --gecos "" appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
