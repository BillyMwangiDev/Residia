# ADR 0001: Residian Backend Foundation

## Status
Accepted

## Context
The repository started as documentation only and needed a production-oriented backend foundation for the Residian platform that can run locally, in CI, and on a managed Docker platform.

## Decision
Use Django + Django REST Framework for the initial API surface, PostgreSQL for persistence, Redis for cache and Celery broker, JWT for authentication, and Docker/GitHub Actions for delivery automation.

## Consequences
- The first release focuses on REST instead of adding GraphQL immediately.
- Payments are abstracted behind a sandbox service first to keep production hardening incremental.
- The project stays modular by separating core, users, properties, bookings, reviews, and payments.
