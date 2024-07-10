from django.http import response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    ProfileUpdateSerializerForUser,
    LoginSerializer,
    ProfileSerializer,
)
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User, Profile
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login, logout
from .permissions import IsOnlyMyProfile
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer, 400: {"default": "Bad request"}},
        description="Регистрация",
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: LoginSerializer, 404: {"default": "Bad request"}},
        description="Логинизация",
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "login successful"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        description="Выход пользователя из системы",
        responses={
            204: {"default": "Выход успешно выполнен"},
            401: {"default": "Ошибка аутентификации"},
        },
    )
    def get(self, request):
        logout(request)
        return Response({"message": "logout successful"}, status=status.HTTP_200_OK)


class UserView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        responses={200: UserSerializer, 404: {"default": "Bad request"}},
        description="Активный в настоящее время юзер",
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        responses={200: UserSerializer, 404: {"default": "Bad request"}},
        description="Все юзеры",
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users)
        return Response(serializer.data)


class ProfileView(generics.ListAPIView):
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        responses={"201": ProfileSerializer, "404": {"default": "Bad request"}},
        description="Активный в настоящее время профиль",
    )
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileUpdate(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializerForUser
    permission_classes = [IsAuthenticated, IsOnlyMyProfile]

    @extend_schema(
        request=ProfileUpdateSerializerForUser,
        responses={
            201: ProfileUpdateSerializerForUser,
            404: {"default": "Bad request"},
        },
        description="Обновление профиля для пользователя",
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ProfileDelete(generics.RetrieveDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOnlyMyProfile]

    @extend_schema(
        request=ProfileSerializer,
        responses={
            204: None,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Удаление профиля",
    )
    def delete_profile(self, request, pk):
        profile = Profile.objects.filter(pk=pk)
        profile.delete()
        response.data = {"message": "Успешно"}
        return response


class ProfileUserForAdminSearchView(APIView):
    @extend_schema(
        request=ProfileSerializer,
        responses={
            201: ProfileSerializer,
            400: {"default": []},
        },
        description="Поиск профиля имени по search_query"
        "среди полей name/phone_number. "
        "Пример: ?search_query=Olya",
    )
    def get(self, request):
        profile = Profile.objects.get(user=self.request.user)
        if profile.role == "Администратор":
            search_query = request.GET.get("search_query", "")
            profiles = Profile.objects.filter(full_name__icontains=search_query)
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data)
        else:
            raise AuthenticationFailed("Не прошедший проверку подлинности!")
