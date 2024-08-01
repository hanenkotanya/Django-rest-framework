from rest_framework.views import APIView
from .serializers import (
    PlayerSerializer,
    LoginSerializer
)
from rest_framework.response import Response
from .models import Player
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.contrib.auth import authenticate, login, logout
from django.conf import settings


class RegisterView(generics.CreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request = PlayerSerializer,
        responses = {
            201: PlayerSerializer,
            400: {"default": "Bad request"}
        },
        description="Регистрация",
    )
    def post(self, request, *args, **kwargs):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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
        player = authenticate(request, email=email, password=password)
        if player is not None:
            login(request, player)
            user = self.request.user
            user.first_entrance = True
            user.save()
            return Response({'message': 'login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    serializer_class = PlayerSerializer
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

