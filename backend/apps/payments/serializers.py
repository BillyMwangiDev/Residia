from rest_framework import serializers

from apps.bookings.models import Booking

from .models import Payment
from .services import SandboxPaymentGateway
from .tasks import notify_payment_processed


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            "id",
            "booking",
            "amount",
            "payment_method",
            "status",
            "transaction_reference",
            "provider_response",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "amount",
            "status",
            "transaction_reference",
            "provider_response",
            "created_at",
            "updated_at",
        )

    def validate_booking(self, booking: Booking):
        request = self.context["request"]
        if (
            booking.guest_id != request.user.id
            and booking.property.host_id != request.user.id
        ):
            raise serializers.ValidationError(
                "You cannot create a payment for this booking."
            )
        if hasattr(booking, "payment"):
            raise serializers.ValidationError(
                "This booking already has a payment record."
            )
        return booking

    def create(self, validated_data):
        booking = validated_data["booking"]
        gateway = SandboxPaymentGateway()
        result = gateway.charge(
            amount=booking.total_price,
            payment_method=validated_data["payment_method"],
        )
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_price,
            payment_method=validated_data["payment_method"],
            status=result.status,
            transaction_reference=result.reference,
            provider_response=result.provider_response,
        )
        notify_payment_processed.delay(payment.id)
        return payment
