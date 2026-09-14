from datetime import date

import pytest
from rest_framework import status


@pytest.mark.django_db
def test_guest_can_book_review_and_pay_for_property(
    api_client, guest_user, property_listing
):
    api_client.force_authenticate(user=guest_user)

    booking_response = api_client.post(
        "/api/bookings/",
        {
            "property": property_listing.id,
            "check_in_date": date(2026, 8, 1),
            "check_out_date": date(2026, 8, 4),
        },
        format="json",
    )
    assert booking_response.status_code == status.HTTP_201_CREATED
    assert booking_response.data["total_price"] == "360.00"

    review_response = api_client.post(
        "/api/reviews/",
        {
            "property": property_listing.id,
            "rating": 5,
            "comment": "Excellent stay with responsive hosting.",
        },
        format="json",
    )
    assert review_response.status_code == status.HTTP_201_CREATED

    payment_response = api_client.post(
        "/api/payments/",
        {
            "booking": booking_response.data["id"],
            "payment_method": "card",
        },
        format="json",
    )
    assert payment_response.status_code == status.HTTP_201_CREATED
    assert payment_response.data["status"] == "succeeded"
    assert payment_response.data["transaction_reference"].startswith("txn_")
