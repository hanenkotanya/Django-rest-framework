from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Profile


class IsOnlyMyProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

class IsOnlyAdministratorOrAnimators(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = Profile.objects.get(user = request.user) 
        return profile.role == "Администратор" or profile.role == "Аниматор"