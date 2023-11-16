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
    

