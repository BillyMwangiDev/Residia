from datetime import date
from decimal import Decimal

import pytest
from rest_framework.exceptions import ValidationError

from apps.bookings.models import Booking
from apps.bookings.services import (
    calculate_total_price,
    ensure_booking_window_available,
)


@pytest.mark.django_db
def test_calculate_total_price_multiplies_nightly_rate():
    total_price = calculate_total_price(nightly_price=Decimal("120.00"), nights=3)

    assert total_price == Decimal("360.00")


def test_calculate_total_price_rejects_zero_nights():
    with pytest.raises(ValidationError):
        calculate_total_price(nightly_price=Decimal("120.00"), nights=0)


@pytest.mark.django_db
def test_ensure_booking_window_available_rejects_overlaps(guest_user, property_listing):
    Booking.objects.create(
        guest=guest_user,
        property=property_listing,
        check_in_date=date(2026, 7, 10),
        check_out_date=date(2026, 7, 14),
        total_price="480.00",
        status=Booking.Status.CONFIRMED,
    )

    with pytest.raises(ValidationError):
        ensure_booking_window_available(
            property_id=property_listing.id,
            check_in_date=date(2026, 7, 12),
            check_out_date=date(2026, 7, 16),
        )
