# Residian Usage Guide

## Local setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up --build
```

## Manual backend commands
```bash
source .venv/bin/activate
cd backend
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Quality and security checks
```bash
black --check .
flake8 .
pytest
pip-audit -r requirements.txt
```

## Deployment notes
- Render/Railway should use managed PostgreSQL and Redis services.
- Set `DEBUG=False`, rotate `SECRET_KEY`, and provide a real `SENTRY_DSN`.
- Run migrations during each deployment before serving traffic.
- Schedule daily backups for the production database and verify restore procedures regularly.
