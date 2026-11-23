# Residian Platform API

Production-oriented Django backend for **Residian**, a short-term rental marketplace platform. The application provides JWT-authenticated APIs for users, properties, bookings, reviews, and sandbox payments, with Docker, Redis, Celery, pytest, flake8, `pip-audit`, and GitHub Actions support.

## Setup Checklist
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
git checkout main
git checkout -b feature/production-overhaul
```

## Project Tree
```text
residian/
|-- backend/
|   |-- apps/
|   |   |-- bookings/
|   |   |-- core/
|   |   |-- payments/
|   |   |-- properties/
|   |   |-- reviews/
|   |   `-- users/
|   |-- config/
|   `-- manage.py
|-- docs/
|   |-- ADRs/
|   `-- usage.md
|-- tests/
|   |-- e2e/
|   |-- integration/
|   `-- unit/
|-- .env.example
|-- .flake8
|-- docker-compose.yml
|-- Dockerfile
|-- pytest.ini
`-- requirements.txt
```

## Technology Stack
- Django + Django REST Framework
- PostgreSQL for production data
- Redis + Celery for cache and async work
- JWT authentication with role-aware authorization
- Docker and Docker Compose for local/dev runtime
- GitHub Actions for lint, test, and security checks

## Implementation
- `users`: custom email-based user model with guest, host, and admin roles
- `properties`: host-managed listings with searchable metadata
- `bookings`: overlap-aware reservation flow with calculated totals
- `reviews`: one review per user per property
- `payments`: sandbox payment abstraction with async notification hook
- `core`: health checks, pagination, request-context logging, and shared utilities

## Environment Variables
Secrets are managed with `python-decouple`. Use `.env.example` as the template and never commit real secrets.

Key variables:
- `SECRET_KEY`
- `DATABASE_URL`
- `REDIS_CACHE_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `ALLOWED_HOSTS`
- `CORS_ALLOWED_ORIGINS`
- `SENTRY_DSN`

## Run Locally
```bash
source .venv/bin/activate
docker compose up --build
```

Or run the backend directly:
```bash
source .venv/bin/activate
cd backend
python manage.py migrate
python manage.py runserver
```

## API Surface
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/token/refresh/`
- `GET/PATCH /api/auth/me/`
- `GET/POST /api/properties/`
- `GET/POST /api/bookings/`
- `GET/POST /api/reviews/`
- `GET/POST /api/payments/`
- `GET /api/core/health/`
- `GET /api/docs/swagger/`

## Minimal Runnable Example
Create a host, log in, and create a property:

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"host@example.com","full_name":"Host User","password":"Password123","role":"host"}'

curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"host@example.com","password":"Password123"}'

curl -X POST http://localhost:8000/api/properties/ \
  -H "Authorization: Bearer <access-token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Ocean View Villa","description":"Private villa with pool.","location":"Mombasa","price_per_night":"250.00","bedrooms":4,"bathrooms":3,"max_guests":8,"is_active":true}'
```

## Testing And Static Analysis
```bash
black --check .
flake8 .
pytest
pip-audit -r requirements.txt
```

## CI
GitHub Actions workflow lives in `.github/workflows/ci.yml` and runs:
- formatting check with `black --check`
- linting with `flake8`
- Django migrations
- pytest with coverage
- dependency scanning with `pip-audit`

## Deployment
This project is optimized for Render or Railway with:
- managed PostgreSQL
- managed Redis
- Docker-based web service deployment
- `gunicorn` for app serving
- environment-based configuration via `.env`

Production recommendations:
- set `DEBUG=False`
- rotate `SECRET_KEY`
- enable HTTPS and host validation
- provide a real `SENTRY_DSN`
- schedule daily database backups and regular restore drills

## Docs
- Architecture decision record: `docs/ADRs/0001-backend-foundation.md`
- Usage notes: `docs/usage.md`

## Suggested Commit Series
- `chore: bootstrap django backend foundation`
- `feat: add marketplace domain models and apis`
- `test: add production-readiness validation suite`
- `chore: add docker ci and deployment assets`
- `docs: rewrite setup and operations guide`