# ContextBridge API — Cloud Run image (P0-9a skeleton; Phase 4 hardens this).
# Build from the REPOSITORY ROOT:  docker build -f api/Dockerfile .
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /srv

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Backend package + the reused in-window modules (provenance: context/PROVENANCE.md).
COPY api/ ./api/
COPY contextbridge_schema.py contextbridge_store.py ./

# Cloud Run injects PORT (default 8080). Fixtures seed at startup (P0-6, Phase 1).
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
