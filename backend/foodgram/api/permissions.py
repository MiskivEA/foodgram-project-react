from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Дает права управления объектами только их владельцам"""
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
