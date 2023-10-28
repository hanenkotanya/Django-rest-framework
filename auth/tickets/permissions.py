from rest_framework import permissions
import jwt
from rest_framework.exceptions import AuthenticationFailed
from users.models import User

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

class IsAdminOrReadOnlyForAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return get_user(request).role == 'Админ' or obj.author == get_user(request)
        return get_user(request).role == 'Админ' 
            
class IsOnlyAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return get_user(request).role == 'Админ' 
 
class IsOnlyAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == get_user(request)