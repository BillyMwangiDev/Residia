from decimal import Decimal

from django.db.models import Q
from rest_framework.exceptions import ValidationError

from apps.properties.models import Property

from .models import Booking


def ensure_booking_window_available(
    *,
    property_id: int,
    check_in_date,
    check_out_date,
    exclude_booking_id=None,
    lock_property: bool = False
) -> None:
    if lock_property:
        # Acquire a row-level lock on the property to serialize concurrent booking requests
        Property.objects.select_for_update().filter(id=property_id).first()

    overlap_query = Q(check_in_date__lt=check_out_date) & Q(
        check_out_date__gt=check_in_date
    )
    queryset = Booking.objects.filter(property_id=property_id).exclude(
        status=Booking.Status.CANCELLED
    )
    if exclude_booking_id is not None:
        queryset = queryset.exclude(pk=exclude_booking_id)
    if queryset.filter(overlap_query).exists():
        raise ValidationError(
            {
                "non_field_errors": [
                    "This property is unavailable for the selected dates."
                ]
            }
        )


def calculate_total_price(*, nightly_price: Decimal, nights: int) -> Decimal:
    if nights < 1:
        raise ValidationError(
            {"check_out_date": ["A booking must be at least one night."]}
        )
    return nightly_price * Decimal(nights)
