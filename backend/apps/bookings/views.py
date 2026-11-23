from django.db.models import Q
from rest_framework import permissions, viewsets

from apps.users.models import User

from .models import Booking
from .permissions import IsBookingOwnerHostOrAdmin
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerHostOrAdmin]
    filterset_fields = ("status", "property")
    ordering_fields = ("check_in_date", "created_at")

    def get_queryset(self):
        queryset = Booking.objects.select_related("guest", "property", "property__host")
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return queryset
        if user.role == User.Role.HOST:
            return queryset.filter(Q(property__host=user) | Q(guest=user)).distinct()
        return queryset.filter(guest=user)
