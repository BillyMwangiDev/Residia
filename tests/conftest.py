import os

os.environ.setdefault("SECRET_KEY", "test-secret-key-with-sufficient-length-123")
os.environ.setdefault("DEBUG", "False")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("ALLOWED_HOSTS", "testserver,localhost,127.0.0.1")
os.environ.setdefault("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
os.environ.setdefault("CSRF_TRUSTED_ORIGINS", "http://localhost:3000")
os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/residian_test.sqlite3")
os.environ.setdefault("CELERY_TASK_ALWAYS_EAGER", "True")

import pytest  # noqa: E402
from rest_framework.test import APIClient  # noqa: E402


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def guest_user(db):
    from apps.users.models import User

    return User.objects.create_user(
        email="guest@example.com",
        password="Password123",
        full_name="Guest User",
        role=User.Role.GUEST,
    )


@pytest.fixture
def host_user(db):
    from apps.users.models import User

    return User.objects.create_user(
        email="host@example.com",
        password="Password123",
        full_name="Host User",
        role=User.Role.HOST,
    )


@pytest.fixture
def property_listing(db, host_user):
    from apps.properties.models import Property

    return Property.objects.create(
        host=host_user,
        title="Nairobi Loft",
        description="A clean city apartment.",
        location="Nairobi",
        price_per_night="120.00",
        bedrooms=2,
        bathrooms=1,
        max_guests=3,
    )
