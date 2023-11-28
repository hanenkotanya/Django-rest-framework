from personage.serializers import PersonageSerializer
from personage.models import Personage
from rest_framework import generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response


class PersonageFor1_4ListView(generics.ListAPIView):
    queryset = Personage.objects.filter(for_age ='1', activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        request=PersonageSerializer,
        responses={
            201: PersonageSerializer,
            204: {"default": []},
            400: {"default": "Bad request"},

        },
        description="Перечень персонажей по категории для 1-4 лет"  
    )
    def get(self, request):
        personage = Personage.objects.filter(for_age = '1', activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)


class PersonageFor5_9ListView(generics.ListAPIView):
    queryset = Personage.objects.filter(for_age ='2', activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        request=PersonageSerializer,
        responses={
            201: PersonageSerializer,
            204: {"default": []},
            400: {"default": "Bad request"},
        },
        description="Перечень персонажей по категории для 5-9 лет"  
    )
    def get(self, request):
        personage = Personage.objects.filter(for_age = '2', activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)
    

class PersonageFor10_14ListView(generics.ListAPIView):
    queryset = Personage.objects.filter(for_age ='3', activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        request=PersonageSerializer,
        responses={
            201: PersonageSerializer,
            204: {"default": []},
            400: {"default": "Bad request"},
        },
        description="Перечень персонажей по категории для 10-14 лет"  
    )
    def get(self, request):
        personage = Personage.objects.filter(for_age = '3', activity = True)
        serializer = PersonageSerializer(personage, many=True)
        return Response(serializer.data)