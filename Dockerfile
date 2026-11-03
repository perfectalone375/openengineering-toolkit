FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
COPY tests/ ./tests/

RUN pip install --upgrade pip && \
    pip install -e ".[api,dev]"

FROM base AS test
CMD ["pytest", "-v", "tests/"]

FROM base AS runtime
EXPOSE 8000
CMD ["uvicorn", "openengineering.api:app", "--host", "0.0.0.0", "--port", "8000"]
