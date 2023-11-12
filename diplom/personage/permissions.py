from rest_framework import permissions
from user.models import Profile


class IsOnlyAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = Profile.objects.get(user =request.user)   #obj это сам персонаж
        return profile.role == 'Администратор'
    


