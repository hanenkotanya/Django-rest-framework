from django.contrib.auth import authenticate
from django.http import response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer, 
    ProfileUpdateSerializerForUser,
    LoginSerializer, 
    ProfileSerializer, 
    ProfileUpdateSerializerForAnimators,
    AnimotorForUserSerializer
)
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Profile, get_avatar_full_path, get_avatar_url
from rest_framework import generics, permissions, status, mixins
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login, logout
from .permissions import IsOnlyMyProfile, IsOnlyAdministratorOrAnimators
from django.db.models import Q
import os
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request = UserSerializer,
        responses = {
            201: UserSerializer,
            400: {"default": "Bad request"}
        },
        description="Регистрация",
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        image = request.FILES.get("image", None)
        if image:
            # Генерируем путь для сохранения аватарки
            imagepath = os.path.join(
                settings.MEDIAROOT, get_avatar_full_path(user, image.name)
            )
            # Сохраняем аватарку по полученному пути
            with open(imagepath, "wb") as f:
                for chunk in image.chunks():
                    f.write(chunk)
            # Обновляем URL аватарки
            user.avatarurl = get_avatar_url(user, image.name)
            # Сохраняем модель пользователя с обновленным полем avatarurl
            user.save(updatefields=["avatarurl"])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request = LoginSerializer,
        responses = {
            200: LoginSerializer,
            404: {"default": "Bad request"}
        },
        description="Логинизация",
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
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,]
    @extend_schema(
        description="Выход пользователя из системы",
        responses={
            204: {"default": "Выход успешно выполнен"},
            401: {"default": "Ошибка аутентификации"},
        },
    )
    def get(self, request):
        logout(request)
        return Response({'message': 'logout successful'}, status=status.HTTP_200_OK)

class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,]
    @extend_schema(
        responses = {
            200: UserSerializer,
            404: {"default": "Bad request"}
        },
        description="Активный в настоящее время юзер",
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    

class ProfileView(generics.ListAPIView):    #профиль активного юзера
    permission_classes=[IsAuthenticated,]
    @extend_schema(
        responses = {
            "201": ProfileSerializer,
            "404": {"default": "Bad request"}
        },
        description="Активный в настоящее время профиль",
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
            201: ProfileUpdateSerializerForUser,
            404: {"default": "Bad request"}
        },
        description="Обновление профиля для пользователя",
    ) 
    def update_profile(self, request, pk, *args, **kwargs):
        profile = Profile.object.filter(pk=pk)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)
    
    @extend_schema(
        request = ProfileUpdateSerializerForUser,
        responses = {
            201: ProfileUpdateSerializerForUser,
            404: {"default": "Bad request"},
        },
        description="Обновление профиля для пользователя",
    ) 
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
class ProfileUpdateForAnimatorsOrAdministrator(generics.UpdateAPIView):    
    queryset = Profile.objects.all()                           
    serializer_class = ProfileUpdateSerializerForAnimators
    permission_classes=[IsAuthenticated, IsOnlyMyProfile, IsOnlyAdministratorOrAnimators ]
    @extend_schema(
        request = ProfileUpdateSerializerForAnimators,
        responses = {
            201: ProfileUpdateSerializerForAnimators,
            404: {"default": "Bad request"},
        },
        description="Обновление профиля для администратора и аниматора",
    ) 
    def update_profile(self, request, pk, *args, **kwargs):
        profile = Profile.object.filter(pk=pk)
        serializer_data = request.data.get(profile)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)
    @extend_schema(
        request = ProfileUpdateSerializerForAnimators,
        responses = {
            201: ProfileUpdateSerializerForAnimators,
            404: {"default": "Bad request"},
        },
        description="Обновление профиля для администратора и аниматора",
    ) 
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    


class ProfileDelete(mixins.DestroyModelMixin, generics.GenericAPIView): 
    queryset = Profile.objects.all()                           
    serializer_class = ProfileSerializer
    permission_classes=[IsAuthenticated, IsOnlyMyProfile]  
    @extend_schema(
        request=ProfileSerializer,
        responses={
            204: None,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Удаление профиля",
    ) 
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)



class AnimatorsListView(generics.ListAPIView):
    queryset = Profile.objects.filter(role = 'Аниматор')
    serializer_class = AnimotorForUserSerializer
    permission_classes = [IsAuthenticated, ]
    @extend_schema(
        responses={
            200: AnimotorForUserSerializer,
            400: {"default": []},
        },
        description="Перечень страниц аниматоров",
    )
    def get(self, request):
        kombo = Profile.objects.filter(role = 'Аниматор') 
        serializer = ProfileSerializer(kombo, many=True)
        return Response(serializer.data)
    
    

class AnimatorsOneListView(generics.RetrieveAPIView):
    queryset = Profile.objects.filter(role = 'Аниматор')
    serializer_class = AnimotorForUserSerializer
    permission_classes = [IsAuthenticated, ]
    @extend_schema(
        responses={
            200: AnimotorForUserSerializer,
            400: {"default": []},
        },
        description="Страница аниматора",
    )
    def get(self, request, pk):
        kombo = Profile.objects.filter(pk=pk)
        serializer = ProfileSerializer(kombo, many=True)
        return Response(serializer.data)

   

class ProfileUserForAdminSearchView(APIView):
    @extend_schema(
        request=ProfileSerializer,
        responses={
            201: ProfileSerializer,
            400: {"default": []},
        },
        description="Поиск профиля по номеру телефона или имени по search_query" 
        "среди полей name/phone_number. "
        "Пример: ?search_query=Olya",
    )
    def get(self, request):
        search_query = request.GET.get("search_query", "")

        profiles = Profile.objects.filter(
            Q(full_name__icontains=search_query)
            | Q(phone_number__icontains=search_query)
        )
        serializer = ProfileSerializer (profiles, many=True)
        return Response(serializer.data)


