from rest_framework.permissions import BasePermission
from rest_framework import permissions
from rest_framework.templatetags import rest_framework


class IsAdminAuthPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_active or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.author
