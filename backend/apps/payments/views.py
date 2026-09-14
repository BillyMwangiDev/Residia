from django.db.models import Q
from rest_framework import permissions, viewsets

from apps.users.models import User

from .models import Payment
from .permissions import IsBookingStakeholderOrAdmin
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingStakeholderOrAdmin]
    http_method_names = ["get", "post", "head", "options"]
    filterset_fields = ("status", "payment_method")
    ordering_fields = ("created_at", "amount")

    def get_queryset(self):
        queryset = Payment.objects.select_related(
            "booking", "booking__guest", "booking__property", "booking__property__host"
        )
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return queryset
        return queryset.filter(
            Q(booking__guest=user) | Q(booking__property__host=user)
        ).distinct()
