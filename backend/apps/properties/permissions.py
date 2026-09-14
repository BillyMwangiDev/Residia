from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.users.models import User


class IsHostOrReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {User.Role.HOST, User.Role.ADMIN}
        )

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.role == User.Role.ADMIN or obj.host_id == request.user.id)
        )
