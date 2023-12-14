from .serializers import (
    PersonageSerializer, 
    KomboSerializer, 
    PersonageUpdateSerializerForAdministrator, 
    LikeSerializer,
    PersonageSearchSerializer, 
    PersonageListSerializer,
    PersonageOneListSerializer
)
from rest_framework.exceptions import AuthenticationFailed
from user.models import Profile
from .models import Personage, Kombo
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from django.http import response
from .permissions import IsOnlyAdministrator
from rest_framework.views import APIView
from django.conf import settings 
from django.db.models import Q



class PersonageCreateView(generics.CreateAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageSerializer
    permission_classes = [IsAuthenticated ]
    @extend_schema(
        request = PersonageSerializer,
        responses = {
            201: PersonageSerializer,
            400: {"default": "Bad request"}
        },
        description="Создание персонажа администратором" ,
    )
    def perform_create(self, serializer):
        profile = Profile.objects.get(user = self.request.user)
        if profile.role == "Администратор":
            serializer.save(creator = self.request.user)
        else:
            raise AuthenticationFailed('Не прошедший проверку подлинности!')


class PersonageListView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True)
    serializer_class = PersonageListSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        responses = {
            200: PersonageListSerializer,
            404: {"default": []},
            400: {"default": "Bad request"},
        },
        description="Перечень персонажей", 
    )
    def get(self, request):
        personage = Personage.objects.filter(activity = True)  
        serializer = PersonageListSerializer(personage, many=True)
        return Response(serializer.data)
   

class PersonageOneListView(generics.RetrieveAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageOneListSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        responses = {
            200: PersonageOneListSerializer,
            404: {"default": []},
            400: {"default": "Bad request"},
        },
        description="Страница одного персонажа", 
    )
    def get(self, request, pk):
        personage = Personage.objects.filter(pk=pk, activity = True)
        serializer = PersonageOneListSerializer(personage, many=True)
        return Response(serializer.data)
    
        

class PersonageOneUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Personage.objects.all()
    serializer_class = PersonageUpdateSerializerForAdministrator
    permission_classes = [IsAuthenticated, IsOnlyAdministrator ]
    @extend_schema(
        request = PersonageUpdateSerializerForAdministrator,
        responses = {
            201: PersonageUpdateSerializerForAdministrator,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Изменение персонажа администратором", 
    )
    def update_personage(self, request, pk):
        personage = Personage.objects.filter(pk=pk) 
        serializer_data = request.data.get(personage)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)

    @extend_schema(
        request = PersonageUpdateSerializerForAdministrator,
        responses = {
            201: PersonageUpdateSerializerForAdministrator,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Изменение персонажа администратором", 
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

@extend_schema_view(get=extend_schema(description="Лайкнуть персонажа")) 
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


@extend_schema_view(get=extend_schema(description="Убрать лайк персонажа"))     
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


@extend_schema_view(get=extend_schema(description="Все лайки активного пользователя")) 
class PersonageLikeListView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True)
    serializer_class = PersonageSerializer
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
        profile = request.user.profile
        my_likes =  profile.my_likes.filter(activity = True)
        serializer = PersonageSerializer(my_likes, many=True)
        return Response(serializer.data)
    
    
class PersonageDeleteView(generics.DestroyAPIView):
    queryset = Personage.objects.all() 
    serializer_class = PersonageSerializer
    permission_classes=[IsAuthenticated, IsOnlyAdministrator]  
    @extend_schema(
        request=PersonageSerializer,
        responses={
            204: None,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Удаление персонажем администратора",
    )  
    def delete_personage(self, request, pk):
        personage = Personage.objects.filter(pk=pk)
        personage.delete()
        response.data = {
            'message': 'Успешно'
        }
        return response
    

class KomboListView(generics.ListAPIView):
    queryset = Kombo.objects.filter(activity = True)
    serializer_class = KomboSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        responses = {
            200: KomboSerializer,
            404: {"default": "Bad request"}
        },
        description="Перечень комбо",
    )
    def get(self, request):
        kombo = Kombo.objects.filter(activity = True)  
        serializer = KomboSerializer(kombo, many=True)
        return Response(serializer.data)
    

class Life_size_puppetListView(generics.ListAPIView):
    queryset = Personage.objects.filter(activity = True)
    serializer_class = PersonageListSerializer
    permission_classes = [AllowAny, ]
    @extend_schema(
        responses = {
            200: KomboSerializer,
            404: {"default": "Bad request"}
        },
        description="Перечень ростовых кукл",
    )
    def get(self, request):
        life_size_puppet = Personage.objects.filter(
        Q(activity = True)
        & Q(life_size_puppet = True)
        )
        serializer = PersonageSerializer(life_size_puppet, many=True)
        return Response(serializer.data)
    


class PersonageSearchView(APIView):
    @extend_schema(
        request=PersonageSearchSerializer,
        responses={
            201: PersonageSearchSerializer,
            400: {"default": []},
        },
        description="Поиск персонажа по search_query среди полей name/personage1/personage2. "
        "Пример: ?search_query=Крош",
    )
    def get(self, request):
        search_query = request.GET.get("search_query", "")

        personages = Personage.objects.filter(name__icontains=search_query)

        serializer = PersonageSearchSerializer(personages, many=True)
        return Response(serializer.data)