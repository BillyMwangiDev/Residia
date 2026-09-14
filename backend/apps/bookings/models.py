from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.properties.models import Property


class Booking(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="bookings"
    )
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)]
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(check_out_date__gt=models.F("check_in_date")),
                name="booking_checkout_after_checkin",
            )
        ]
        indexes = [
            models.Index(fields=["property", "check_in_date", "check_out_date"]),
            models.Index(fields=["guest", "status"]),
        ]

    def clean(self):
        super().clean()
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

    def __str__(self) -> str:
        return f"{self.property} ({self.check_in_date} - {self.check_out_date})"


# Create your models here.
