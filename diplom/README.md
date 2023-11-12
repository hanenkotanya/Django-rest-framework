1 commit 

pip install django
django-admin startproject diplom
cd diplom
pip inctall virtualenv
virtualenv venv
source venv/bin/activate
pip install djangorestframework
pip install django-cors-headers
pip install Pillow
pip install drf-spectacular
pip install django-rest-swagger
python manage.py startapp user

В diplom.settings.py import os
LANGUAGE_CODE = 'ru'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
В INSTALLED_APPS добавляем
    'rest_framework',
    'corsheaders',
    'users',
    'rest_framework_swagger',
    'drf_spectacular'
В MIDDLEWARE добавляем
    'corsheaders.middleware.CorsMiddleware',
    НАД
    'django.middleware.common.CommonMiddleware',
Определяем своего юзера 
AUTH_USER_MODEL = 'users.User' # TODO register user
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

Создали в users urls.py

В корневом urls.py проекта добавили include на users.urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema' ),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),   
]

Создали файлы urls.py, serializers.py, signals.py в приложении users
В файле models.py приложения users.py сделали необходимые импорты и создали модель юзера и модель профиля

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
import uuid


class User(AbstractUser):
    password = models.CharField(max_length=255)
    slug =  models.SlugField(unique=True, verbose_name='Слаг', blank=True, null=True)
    email = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] #TODO

    def  generate_slug(self):
        return slugify(self.email)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args,**kwargs)
    
    objects = UserManager()



class Profile(models.Model):
    ROLE_CHOICES = (
        ('Пользователь', 'Пользователь'),
        ('Админ', 'Админ'),
        ('Аниматор', 'Аниматор')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Пользователь')
    email = models.EmailField(max_length=100, blank=True, null=True, unique=True)
    intro = models.CharField(max_length=50, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True,
                              default='profile_images/default.jpg',
                              upload_to='profile_images')
    tiktok = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    objects = UserManager()

    def __str__(self):
        return str(self.user)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

В файле serializers.py приложения users сделали необходимые импорты и создали LoginSerializer, UserSerializer
ProfileSerializer, ProfileUpdateSerializerForUser, ProfileUpdateSerializerForAnimators

from rest_framework import serializers
from .models import User, Profile
from rest_framework.exceptions import ValidationError

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            return data
        else:
            raise serializers.ValidationError('не правильные данные')
        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'slug', 'username']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.get('email')
        username = validated_data.get('username')
        try:
            user = User.objects.create_user(email=email, password=password, username=username)
        except ValidationError as e:
            raise serializers.ValidationError({'email': e})
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'email', 'role', 'intro', 'username']


class ProfileUpdateSerializerForUser(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user','image', 'email','username']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'email': {'read_only': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance
    

class ProfileUpdateSerializerForAnimators(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user','image', 'email','username', 'intro']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
            'email': {'read_only': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance

В файле signals.py приложения users сделали необходимые импорты и создали сигналы для автоматического создания профиля при создании юзера(и удалении при удалении юзера)

from django.db.models.signals import post_save, post_delete
from .models import User
from .models import Profile
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            email=user.email,
            username = user.username

        )


def updateProfile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == True:
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateProfile, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)

В файле apps.py приложения users установили сигналы
    def ready(self):
        import users.signals

В users.views.py сделали необходимые импорты и написали представления
from django.contrib.auth import authenticate
from django.http import response
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileUpdateSerializerForUser,LoginSerializer, ProfileSerializer, ProfileUpdateSerializerForAnimators
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Profile
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login, logout
from .permissions import IsOnlyMyProfile, IsOnlyAdministratorOrAnimators



@extend_schema(
        request = UserSerializer,
        responses = {
            "201": UserSerializer,
            "404": "Bad request"
        }
    )
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
 


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,]
    def get(self, request):
        logout(request)
        return Response({'message': 'logout successful'}, status=status.HTTP_200_OK)

class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

 
    def update_profile(self, request, *args, **kwargs):
        user = request.user
        serializer_data = request.data.get(user)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)
    

class ProfileView(generics.ListAPIView):    #профиль активного юзера
    permission_classes=[IsAuthenticated,]
    @extend_schema(
        request = ProfileSerializer,
        responses = {
            "201": ProfileSerializer,
            "404": "Bad request"
        }
    )
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    
class ProfileUpdate(generics.UpdateAPIView):    #функция для изменения данных профиля и юзера 
    queryset = Profile.objects.all()                           
    serializer_class = ProfileUpdateSerializerForUser
    permission_classes=[IsAuthenticated,IsOnlyMyProfile]
    @extend_schema(
        request = ProfileUpdateSerializerForUser,
        responses = {
            "201": ProfileUpdateSerializerForUser,
            "404": "Bad request"
        }
    ) 
    def update_profile(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=pk) 
        profile = Profile.object.filter(user=user)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)

    
class ProfileDelete(generics.RetrieveDestroyAPIView): 
    queryset = Profile.objects.all()                           
    serializer_class = ProfileSerializer
    permission_classes=[IsAuthenticated, IsOnlyMyProfile]   
    def delete_profile(self, request, pk):
        user = User.objects.filter(pk=pk)

        user.delete()
        response.data = {
            'message': 'Успешно'
        }
        return response
    


В user.admin.py 
from django.contrib import admin
from .models import User, Profile

admin.site.register(User)
admin.site.register(Profile)

В user.urls.py

from django.urls import path
from .views import RegisterView, LoginView, UserView, ProfileUpdate, ProfileView, ProfileDelete, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view()),
    path('my_profile/', ProfileView.as_view()),
    path('my_profile_update/<str:pk>/', ProfileUpdate.as_view()),
    path('my_profile_delete/<str:pk>/', ProfileDelete.as_view()),

]

Добавила пердставление на возможность аниматорам и администратору менять поле intro в профиле 

class ProfileUpdateForAnimatorsOrAdministrator(generics.UpdateAPIView):    
    queryset = Profile.objects.all()                           
    serializer_class = ProfileUpdateSerializerForAnimators
    permission_classes=[IsAuthenticated, IsOnlyMyProfile, IsOnlyAdministratorOrAnimators]
    @extend_schema(
        request = ProfileUpdateSerializerForAnimators,
        responses = {
            "201": ProfileUpdateSerializerForAnimators,
            "404": "Bad request"
        }
    ) 
    def update_profile(self, request, pk, *args, **kwargs):
        user = User.objects.filter(pk=pk) 
        profile = Profile.object.filter(user=user)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)

Добавила путь в urls.py приложения

...
path('my_profile_update_for_animators_or_administartor/<str:pk>/', ProfileUpdateForAnimatorsOrAdministrator.as_view()),
...

В файл user.permissions.py добавила ограничение на активного юзера и на действие доступное только аниматорам и администраторам

from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class IsOnlyMyProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsOnlyAdministratorOrAnimators(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = Profile.objects.get(user = request.user) 
        return profile.role == "Администратор" or profile.role == "Аниматор"

Добавила это ограничения в user.views.py ProfileUpdate, ProfileUpdateForAnimatorsOrAdministrator, ProfileDelete. 


python manage.py startapp personage

В dilom.settings.py зарегистрировать приложение personage в INSTALLED_APPS

В diplom.urls.py добавить путь 
path('api/personage/', include('personage.urls')),

В personage создать файлы urls.py, serializers.py, permissions.py

В personage.models.py создаем модель

from django.db import models
from user.models import User


class Personage(models.Model):
    creator = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True, verbose_name='Создатель')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    description = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True,
                              default='personage_images/default.jpg',
                              upload_to='personage_images', verbose_name='Фото')
    activity = models. BooleanField(default=True, verbose_name='Активность')
    life_size_puppet = models. BooleanField(default=False, verbose_name='Ростовая кукла')

    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

Регистрируем модель в админ панели. В файле personage.admin.py 

from django.contrib import admin
from .models import Personage

admin.site.register(Personage)

В views.py делаем необходимые импорты и создаем представления на создание и показ персонажа с ограничением что это может делать только администратор

from django.contrib.auth import authenticate
from .serializers import PersonageSerializer 
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
from .models import Personage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .permissions import IsOnlyAdministrator
from rest_framework.response import Response

def get_user(request):
    try:
        user = User.objects.get(email=request.user)
        return user
    except:
        raise AuthenticationFailed('Не прошедший проверку подлинности!')
        

@extend_schema(
        request = PersonageSerializer,
        responses = {
            "201": Personage,
            "404": "Bad request"
        }
    )

class PersonageCreateView(generics.CreateAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageSerializer
    permission_classes = [IsOnlyAdministrator, ]
    def perform_create(self, serializer):
        serializer.save(creator = get_user(self.request))


class PersonageListView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(activity = True)  
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)


class PersonageOneListView(generics.RetrieveAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request, pk):
        personage = Personage.objects.filter(pk=pk)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)

В serializers.py делаем необходимые импорты и создем сериализатор

from rest_framework import serializers
from .models import Personage
from rest_framework.exceptions import ValidationError

class PersonageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    class Meta:
        model = Personage
        fields = ['id', 'creator', 'name', 'description', 'image', 'activity', 'life_size_puppet']
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True},
            'activity': {'read_only': True},
            'life_size_puppet' : {'read_only': True},
        }

В personage.permissions.py делаем необходимые импорты и создаем пермишен на разрешение действия только Администратору

from rest_framework import permissions
from user.models import Profile


class IsOnlyAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = Profile.objects.get(user =request.user)   
        return profile.role == 'Администр

В views.py пишем представления

class PersonageOneUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageUpdateSerializerForAdministrator
    permission_classes = [IsAuthenticated, IsOnlyAdministrator, ]
    def update_personage(self, request, pk):
        personage = Personage.objects.filter(pk=pk) 
        self.check_object_permissions(self.request, personage)
        serializer_data = request.data.get(personage)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)


class PersonageDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Personage.objects.all() 
    serializer_class = PersonageSerializer
    permission_classes=[IsAuthenticated, IsOnlyAdministrator]   
    def delete_personage(self, request, pk):
        personage = Personage.objects.filter(pk=pk)
        personage.delete()
        response.data = {
            'message': 'Успешно'
        }
        return response

В urls.py делаем необходимые импорты и пишем пути

from django.urls import path
from .views import PersonageCreateView, PersonageListView, PersonageOneListView, PersonageOneUpdateView, PersonageDeleteView 


urlpatterns = [
    path('create_personage/', PersonageCreateView.as_view(), name='create_personage'),
    path('personage_list/', PersonageListView.as_view()),
    path('personage_one/<int:pk>/', PersonageOneListView.as_view()),
    path('personage_one_update/<int:pk>/', PersonageOneUpdateView.as_view()),
    path('personage_one_delete/<int:pk>/', PersonageDeleteView.as_view()),

]

Добавим поля в personage.models.py
    animators_1_4_years = models. BooleanField(default=False, verbose_name='Аниматоры для 1-4 года')
    animators_5_9_years = models. BooleanField(default=False, verbose_name='Аниматоры для 5-9 года')
    animators_9_14_years = models. BooleanField(default=False, verbose_name='Аниматоры для 9-14 года')
Сделала миграции
python manage.py makemigrations
python manage.py migrate


Сделаем представления для показа данных категорий в personage.views.py

class PersonafeListFor1_4_yearsView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True, animators_1_4_years = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(activity = True, animators_1_4_years = True)  
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)
    

class PersonafeListFor9_14_yearsView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True, animators_9_14_years = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(activity = True, animators_9_14_years = True)  
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)
    

class PersonafeListFor5_9_yearsView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True, animators_5_9_years = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(activity = True, animators_5_9_years = True)  
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)


Проимпортируем эти представления и пропишем пути в personage.urls.py

    path('personage_list_for1_4_years/', PersonafeListFor1_4_yearsView.as_view()),
    path('personage_list_for5_9_years/', PersonafeListFor5_9_yearsView.as_view()),
    path('personage_list_for9_14_years/', PersonafeListFor9_14_yearsView.as_view()),
