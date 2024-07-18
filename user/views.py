from django.http import response
from rest_framework.views import APIView
from .serializers import (
    UserSerializer,
    LoginSerializer,
)
from rest_framework.response import Response
from .models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login, logout
from .permissions import IsOnlyMyUser


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


class UserDelete(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOnlyMyUser]

    @extend_schema(
        request=UserSerializer,
        responses={
            204: None,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Удаление юзера",
    )
    def delete_profile(self, request):
        user = self.request.user
        user.delete()
        response.data = {"message": "Успешно"}
        return response
