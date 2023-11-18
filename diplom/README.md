
'''
#pip install django
##django-admin startproject diplom
#cd diplom
#pip inctall virtualenv
#virtualenv venv
#source venv/bin/activate
#pip install djangorestframework
#pip install django-cors-headers
#pip install Pillow
#pip install drf-spectacular
#pip install django-rest-swagger
##python manage.py startapp user
'''

В diplom.settings.py 
'''
import os
LANGUAGE_CODE = 'ru'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
'''
В INSTALLED_APPS добавляем
'''
    'rest_framework',
    'corsheaders',
    'users',
    'rest_framework_swagger',
    'drf_spectacular'
'''
В MIDDLEWARE добавляем
'''
    'corsheaders.middleware.CorsMiddleware',
    _НАД_
    'django.middleware.common.CommonMiddleware',
'''
Определяем своего юзера 
'''
AUTH_USER_MODEL = 'users.User' # TODO register user
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
'''
Создали в users urls.py

В корневом urls.py проекта добавили include на users.urls.py
'''
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularRedocView,
    SpectacularSwaggerView,
    SpectacularAPIView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema' ),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema')),   
]
'''
Создали файлы urls.py, serializers.py, signals.py в приложении user
В файле models.py приложения user.py сделали необходимые импорты и создали модель юзера и модель профиля
'''
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
    name = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Пользователь')
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
'''
В файле serializers.py приложения users сделали необходимые импорты и создали LoginSerializer, UserSerializer
ProfileSerializer, ProfileUpdateSerializerForUser, ProfileUpdateSerializerForAnimators
'''
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
        fields = ['id', 'user', 'image', 'role', 'intro', 'name', 'my_likes']


class ProfileLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['my_likes']


class ProfileUpdateSerializerForUser(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user','image','name']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
    
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance
    

class ProfileUpdateSerializerForAnimators(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user','image', 'name', 'intro']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},

        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance
'''
В файле signals.py приложения users сделали необходимые импорты и создали сигналы для автоматического создания профиля при создании юзера(и удалении при удалении юзера)
'''
from django.db.models.signals import post_save, post_delete
from .models import User
from .models import Profile
from django.conf import settings

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            name = user.username
        )

def updateProfile(sender, instance, created, **kwargs):
    user = instance.user
    profile = Profile.objects.get(user=user)
    user.username = profile.name 
    user.save()

def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, weak=False, sender=User)
post_save.connect(updateProfile, weak=False, sender=Profile)
post_delete.connect(deleteUser, weak=False, sender=Profile)
'''
В файле apps.py приложения users установили сигналы
''' 
    def ready(self):
        import users.signals
'''
В users.views.py сделали необходимые импорты и написали представления
'''
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


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request = UserSerializer,
        responses = {
            "201": UserSerializer,
            "404": "Bad request"
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
 

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request = LoginSerializer,
        responses = {
            "201": LoginSerializer,
            "404": "Bad request"
        }
    )
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

    
class ProfileUpdate(generics.UpdateAPIView):    
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
        profile = Profile.object.filter(pk=pk)
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
        profile = Profile.objects.filter(pk=pk)
        profile.delete()
        response.data = {
            'message': 'Успешно'
        }
        return response
'''

В user.admin.py 
'''
from django.contrib import admin
from .models import User, Profile

admin.site.register(User)
admin.site.register(Profile)
'''
В user.urls.py
'''
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
'''
Добавила пердставление на возможность аниматорам и администратору менять поле intro в профиле 
'''
class ProfileUpdateForAnimatorsOrAdministrator(generics.UpdateAPIView):    
    queryset = Profile.objects.all()                           
    serializer_class = ProfileUpdateSerializerForAnimators
    permission_classes=[IsAuthenticated, IsOnlyMyProfile, IsOnlyAdministratorOrAnimators ]
    @extend_schema(
        request = ProfileUpdateSerializerForAnimators,
        responses = {
            "201": ProfileUpdateSerializerForAnimators,
            "404": "Bad request"
        }
    ) 
    def update_profile(self, request, pk, *args, **kwargs):
        profile = Profile.object.filter(pk=pk)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)
'''

Добавила путь в urls.py приложения
'''
...
path('my_profile_update_for_animators_or_administartor/<str:pk>/', ProfileUpdateForAnimatorsOrAdministrator.as_view()),
...
'''

В файл user.permissions.py добавила ограничение на активного юзера и на действие доступное только аниматорам и администраторам
'''
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
'''

Добавила это ограничения в user.views.py ProfileUpdate, ProfileUpdateForAnimatorsOrAdministrator, ProfileDelete. 


##python manage.py startapp personage


В dilom.settings.py зарегистрировать приложение personage в INSTALLED_APPS

В diplom.urls.py добавить путь 
'''
path('api/personage/', include('personage.urls')),
'''

В personage создать файлы urls.py, serializers.py, permissions.py

В personage.models.py создаем модель
'''
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
'''

Регистрируем модель в админ панели. В файле personage.admin.py 
'''
from django.contrib import admin
from .models import Personage

admin.site.register(Personage)
'''

В views.py делаем необходимые импорты и создаем представления на создание и показ персонажа с ограничением что это может делать только администратор
'''
from django.contrib.auth import authenticate
from .serializers import PersonageSerializer, PersonageUpdateSerializerForAdministrator, LikeSerializer
from rest_framework.exceptions import AuthenticationFailed
from user.models import User, Profile
from .models import Personage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.http import response
from .permissions import IsOnlyAdministrator


class PersonageCreateView(generics.CreateAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageSerializer
    permission_classes = [IsAuthenticated ]
    @extend_schema(
        request = PersonageSerializer,
        responses = {
            "201": Personage,
            "404": "Bad request"
        }
    )
    def perform_create(self, serializer):
        profile = Profile.objects.get(user = self.request.user)
        if profile.role == "Администратор":
            serializer.save(creator = self.request.user)
        else:
            raise AuthenticationFailed('Не прошедший проверку подлинности!')


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
        personage = Personage.objects.filter(pk=pk, activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)
'''

В serializers.py делаем необходимые импорты и создaем сериализатор
'''
from rest_framework import serializers
from .models import Personage
from user.models import Profile
from rest_framework.exceptions import ValidationError

class PersonageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    class Meta:
        model = Personage
        fields = ['id', 'creator', 'name', 'description', 'image', 'activity', 'life_size_puppet', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True},
            'activity': {'read_only': True},
            'life_size_puppet' : {'read_only': True},

        }
'''

В personage.permissions.py делаем необходимые импорты и создаем пермишен на разрешение действия только Администратору
'''
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from user.models import User, Profile


class IsOnlyAdministrator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        profile = Profile.objects.get(user = request.user) 
        return profile.role == "Администратор"
'''

В views.py пишем представления
'''
class PersonageOneUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageUpdateSerializerForAdministrator
    permission_classes = [IsAuthenticated, IsOnlyAdministrator ]
    @extend_schema(
        request = PersonageUpdateSerializerForAdministrator,
        responses = {
            "201": Personage,
            "404": "Bad request"
        }
    )
    def update_personage(self, request, pk):
        personage = Personage.objects.filter(pk=pk) 
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
'''

В urls.py делаем необходимые импорты и пишем пути
'''
from django.urls import path
from .views import PersonageCreateView, PersonageListView, PersonageOneListView, PersonageOneUpdateView, PersonageDeleteView 

urlpatterns = [
    path('create_personage/', PersonageCreateView.as_view(), name='create_personage'),
    path('personage_list/', PersonageListView.as_view()),
    path('personage_one/<int:pk>/', PersonageOneListView.as_view()),
    path('personage_one_update/<int:pk>/', PersonageOneUpdateView.as_view()),
    path('personage_one_delete/<int:pk>/', PersonageDeleteView.as_view()),
]
'''

В модель Profile добавили поле
'''
my_likes = models.ManyToManyField('personage.Personage', symmetrical = False, blank=True, related_name ='who_liked')
'''

Провели миграции

personage.serializers.py
'''
from user.models import Profile

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['my_likes']
        extra_kwargs = {
            'my_likes': {'read_only': True},
        }
'''

personage.views.py
'''
from .serializers import ..., LikeSerializer

class PersonageOneLikeView(generics.RetrieveUpdateAPIView):
    queryset = Personage.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]
    def update(self, request, pk):
        profile = request.user.profile
        personage = Personage.objects.get(pk=pk)
        profile.my_likes.add(personage.id)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)
    

class PersonageOneLikeDeleteView(generics.RetrieveUpdateAPIView):
    queryset = Personage.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated, ]
    def update(self, request, pk):
        profile = request.user.profile
        personage = Personage.objects.get(pk=pk)
        profile.my_likes.remove(personage.id)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)


class PersonageLikeListView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        profile = request.user.profile
        my_likes =  profile.my_likes.filter(activity = True)
        serializer = PersonageSerializer(my_likes, many=True)
        return Response(serializer.data)
'''   

personage.urls.py
'''
from .views import PersonageOneLikeView, PersonageOneLikeDeleteView

urlpatterns = [
    ...
    path('personage_one/<int:pk>/like/', PersonageOneLikeView.as_view()),
    path('personage_one/<int:pk>/like_delete/', PersonageOneLikeDeleteView.as_view()),
    ...
]
'''

user.urls.py
'''
from personage.views import PersonageLikeListView

urlpatterns = [
    ...
    path('my_likes/', PersonageLikeListView.as_view()),
    ...
]
'''

##python manage.py startapp age

В diplom.settings.py 
В INSTALLED_APPS добавляем
'''
    ...
    'age',
    ...
'''

В корневом urls.py добавляем 
'''
    ...
    path('api/personage_for_age/', include('age.urls')),
    ...
'''

В age.models.py создаем модель
'''
from django.db import models


class Age(models.Model):
    AGE_CHOICES = (
        ('choises', 'choises'),
        ('1_4', 'Animators for 1-4 years'),
        ('5_9', 'Animators for 5-9 years'),
        ('10_14', 'Animators for 10-14 years')
    )
    age = models.CharField(max_length=50, choices=AGE_CHOICES, default='choises')
    animators_for_years = models.ManyToManyField('personage.Personage', blank=True, related_name ='for_age')

    
    def __str__(self):
        
        return str(self.age)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
'''

В age.serializers.py
'''
from rest_framework import serializers
from .models import Age
from rest_framework.exceptions import ValidationError

class AgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Age
        fields = ['animators_for_years' ]
        extra_kwargs = {
            'animators_for_years': {'read_only': True},
        }
'''

В age.views.py
'''
from django.contrib.auth import authenticate
from personage.serializers import PersonageSerializer
from .serializers import AgeSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import Age
from personage.models import Personage
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.http import response
from drf_spectacular.utils import extend_schema

class PersonageFor1_4ListView(generics.ListAPIView):
    queryset = Personage.objects.filter(for_age ='1', activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(for_age = '1', activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)


class PersonageFor5_9ListView(generics.ListAPIView):
    queryset = Personage.objects.filter(for_age ='2', activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(for_age = '2', activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)
    

class PersonageFor10_14ListView(generics.ListAPIView):
    queryset = Personage.objects.filter(for_age ='3', activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    def get(self, request):
        personage = Personage.objects.filter(for_age = '3', activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)
'''

В age.urls.py
'''
from django.urls import path
from .views import PersonageFor1_4ListView, PersonageFor5_9ListView, PersonageFor10_14ListView

urlpatterns = [
    path('1_4/', PersonageFor1_4ListView.as_view()),
    path('5_9/', PersonageFor5_9ListView.as_view()),
    path('10_14/', PersonageFor10_14ListView.as_view())
    
] 
'''
Провели миграции