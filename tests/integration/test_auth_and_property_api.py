import pytest
from rest_framework import status


@pytest.mark.django_db
def test_user_can_register_and_login(api_client):
    register_response = api_client.post(
        "/api/auth/register/",
        {
            "email": "new-user@example.com",
            "full_name": "New User",
            "password": "Password123",
            "role": "guest",
        },
        format="json",
    )

    assert register_response.status_code == status.HTTP_201_CREATED

    login_response = api_client.post(
        "/api/auth/login/",
        {"email": "new-user@example.com", "password": "Password123"},
        format="json",
    )

    assert login_response.status_code == status.HTTP_200_OK
    assert "access" in login_response.data


@pytest.mark.django_db
def test_host_can_create_property(api_client, host_user):
    api_client.force_authenticate(user=host_user)

    response = api_client.post(
        "/api/properties/",
        {
            "title": "Ocean View Villa",
            "description": "Private villa with pool.",
            "location": "Mombasa",
            "price_per_night": "250.00",
            "bedrooms": 4,
            "bathrooms": 3,
            "max_guests": 8,
            "is_active": True,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["host_id"] == host_user.id


@pytest.mark.django_db
def test_guest_cannot_create_property(api_client, guest_user):
    api_client.force_authenticate(user=guest_user)

    response = api_client.post(
        "/api/properties/",
        {
            "title": "Not Allowed",
            "description": "Guests should not create listings.",
            "location": "Kisumu",
            "price_per_night": "100.00",
            "bedrooms": 1,
            "bathrooms": 1,
            "max_guests": 2,
            "is_active": True,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
