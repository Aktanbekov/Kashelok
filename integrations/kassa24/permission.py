from rest_framework.permissions import BasePermission


class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        return bool(request.user.id == obj.user)
