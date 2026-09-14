from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import TimeStampedModel
from apps.properties.models import Property


class Review(TimeStampedModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "property"],
                name="unique_review_per_author_and_property",
            )
        ]
        indexes = [models.Index(fields=["property", "rating"])]

    def __str__(self) -> str:
        return f"{self.property} - {self.rating}"


# Create your models here.
