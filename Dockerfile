FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml uv.lock ./
COPY app/ ./app/

RUN uv sync --frozen --no-dev

ENV LOG_LEVEL="INFO"
ENV ENV="prod"
ENV DATABASE_HOST="localhost"
ENV DATABASE_PORT="5432"
ENV DATABASE_USER="postgres"
ENV DATABASE_PASSWORD=""
ENV DATABASE_NAME="test_latam"

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]