from rest_framework import permissions
import jwt
from rest_framework.exceptions import AuthenticationFailed
from .models import User

def get_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Не прошедший проверку подлинности!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Не прошедший проверку подлинности!')
    user = User.objects.filter(id=payload['id']).first()
    return user

class IsOnlyRequestUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == get_user(request) 