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