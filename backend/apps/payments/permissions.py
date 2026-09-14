from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.users.models import User


class IsBookingStakeholderOrAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.role == User.Role.ADMIN:
            return True
        booking = obj.booking
        return (
            booking.guest_id == request.user.id
            or booking.property.host_id == request.user.id
        )
