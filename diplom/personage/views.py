from django.contrib.auth import authenticate
from .serializers import PersonageSerializer, PersonageUpdateSerializerForAdministrator
from rest_framework.exceptions import AuthenticationFailed
from user.models import User
from .models import Personage
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from .permissions import IsOnlyAdministrator
from rest_framework.response import Response
from django.http import response


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
    permission_classes = [IsAuthenticated, IsOnlyAdministrator, ]
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