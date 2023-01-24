from rest_framework.permissions import BasePermission
from  rest_framework import  permissions

class IsActivePermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active)


class AuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user:
            return True
        return False

