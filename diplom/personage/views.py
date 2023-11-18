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
    
    


