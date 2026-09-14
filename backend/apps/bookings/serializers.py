from django.db import transaction
from rest_framework import serializers

from apps.properties.models import Property

from .models import Booking
from .services import calculate_total_price, ensure_booking_window_available


class BookingSerializer(serializers.ModelSerializer):
    guest_id = serializers.IntegerField(source="guest.id", read_only=True)
    property_title = serializers.CharField(source="property.title", read_only=True)

    class Meta:
        model = Booking
        fields = (
            "id",
            "guest_id",
            "property",
            "property_title",
            "check_in_date",
            "check_out_date",
            "total_price",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "guest_id",
            "property_title",
            "total_price",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        property_obj = attrs.get("property") or self.instance.property
        check_in_date = attrs.get("check_in_date") or self.instance.check_in_date
        check_out_date = attrs.get("check_out_date") or self.instance.check_out_date
        ensure_booking_window_available(
            property_id=property_obj.id,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            exclude_booking_id=self.instance.id if self.instance else None,
        )
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        property_obj: Property = validated_data["property"]
        check_in_date = validated_data["check_in_date"]
        check_out_date = validated_data["check_out_date"]
        nights = (check_out_date - check_in_date).days
        validated_data["guest"] = request.user
        validated_data["total_price"] = calculate_total_price(
            nightly_price=property_obj.price_per_night,
            nights=nights,
        )
        with transaction.atomic():
            ensure_booking_window_available(
                property_id=property_obj.id,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                lock_property=True,
            )
            return super().create(validated_data)
