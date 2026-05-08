# User Management API for Latam Technical Assessment

FastAPI-based user management API with hexagonal architecture.

## Quickstart

You can run the application locally in two ways:
1. With Docker Compose
2. With UV


### Running with Docker Compose

```bash
# Start API and PostgreSQL
docker compose up --build
```

### Running Locally with UV

```bash
# Install all dependencies
uv sync

# Run database migrations
uv run alembic upgrade head

# Start the development server
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Environment Variables

To improve security and readability, it is recommended to use environment variables to configure the application. 

| Variable | Description | Default |
|----------|-------------|---------|
| `ENV` | Environment (dev/prod) | `dev` |
| `DATABASE_HOST` | PostgreSQL host | `localhost` |
| `DATABASE_PORT` | PostgreSQL port | `5432` |
| `DATABASE_USER` | PostgreSQL user | `postgres` |
| `DATABASE_PASSWORD` | PostgreSQL password | `postgres` |
| `DATABASE_NAME` | Database name | `test_latam` |
| `DATABASE_URL` | Full database URL | Auto-generated |
| `BASE_URL` | Base URL for the API | `http://localhost:8000` |
| `ALLOWED_CORS_ORIGINS` | CORS allowed origins | `http://localhost:8000,http://localhost:3000` |

Copy `.env.example` to `.env` and adjust as needed.

```bash
cp .env.example .env
```

## API Endpoints

All routes in project are documented here, you can also check them in http://localhost:8000/docs (Swagger UI) or http://localhost:8000/redoc (ReDoc)

### Create User

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Juan Pérez",
    "email": "juan.perez@onemail.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "user",
    "active": true
  }'
```

### Get User by ID

```bash
curl -X GET http://localhost:8000/users/{user_id}
```

### List Users (with Pagination)

```bash
curl -X GET "http://localhost:8000/users?active_only=true&limit=50&offset=0"
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `active_only` | bool | `true` | Filter to active users only |
| `limit` | int | `50` | Max records to return (max: 100) |
| `offset` | int | `0` | Number of records to skip |

### Update User

```bash
curl -X PUT http://localhost:8000/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "username": "Juan Pérez",
    "email": "jperez@twomail.com",
    "first_name": "Juan",
    "last_name": "Pérez",
    "role": "admin",
    "active": true
  }'
```

### Delete User (Soft Delete)

```bash
curl -X DELETE http://localhost:8000/users/{user_id}
```

## Available Routes

| Route | Description |
|-------|-------------|
| `/` | Root endpoint |
| `/users` | User CRUD operations |
| `/health` | Liveness check |
| `/health/db` | Database health check |
| `/ready` | Readiness check |
| `/docs` | OpenAPI documentation |
| `/redoc` | ReDoc documentation |
| `/openapi.json` | OpenAPI schema |

## Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run with coverage report
uv run pytest --cov=app --cov-report=term-missing
```

## Check Code Quality

All code is checked with ruff, black and mypy for code quality and security.

```bash
# Lint with ruff
uv run ruff check .

# Format with black
uv run black .

# Type check with mypy
uv run mypy .

# Run all checks
uv run ruff check . && uv run black . && uv run mypy .
```

## Database Migrations

The database schema is managed using Alembic. Migrations are automatically generated and applied when the application starts.

```bash
# Upgrade to latest
uv run alembic upgrade head

```

## Limitations & Next Steps

- **No authentication/JWT**: Currently no auth implemented. Add pyJWT for production.
- **No rate limiting UI**: Consider adding admin dashboard for rate limit config.
- **Add security code scanning**: Add security code scanning to the project, with tools like SonarQube and Checkmarx.
- **Add monitoring** Add monitoring using cloudwatch, with logs, metrics, traces and alerts.
- **Add CI/CD** Add CI/CD pipeline using GitHub Actions, to run tests, security code scanning and deployment to Google Cloud Run.

## Tech Stack

- **Python** 3.13+
- **FastAPI** - Web framework
- **SQLAlchemy 2.x** - Async ORM
- **Alembic** - Database migrations
- **Pydantic v2** - Data validation
- **PostgreSQL** - Database
- **uv** - Package manager
- **pytest** - Testing framework