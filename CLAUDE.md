# Residian — Platform API

Production-oriented **Django backend** for Residia, a short-term rental marketplace.
JWT-authenticated APIs for users, properties, bookings, reviews and sandbox payments.

Pairs with `~/WORK/Residia-front-end/` — the React client. Same product, two repos.

## Stack

Django + Django REST Framework, PostgreSQL, Redis, Celery. Docker Compose for local services.
pytest, flake8 and `pip-audit` in CI via GitHub Actions.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d      # Postgres + Redis
pytest
```

## Layout

- `backend/` — Django project and apps
- `tests/` — pytest suite (`pytest.ini` at root)
- `docs/` — API and setup documentation
- `Dockerfile`, `docker-compose.yml`

## Working notes

**Name confusion is the main hazard here.** The repo folder is `residian`, the remote is
`BillyMwangiDev/Residia`, and the front end is a separate repo. Check which one you are in
before running migrations or pushing.

Last commit is **2025-10-19** — by far the oldest project in `~/WORK/`, and the front end has
moved since. Expect drift between the API contract and what the client expects; verify against
the running API rather than the docs.

Payments are sandbox-only. Confirm that is still true before pointing anything at real
credentials.
