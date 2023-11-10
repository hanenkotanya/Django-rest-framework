from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class IsOnlyMyProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user