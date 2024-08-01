from django.shortcuts import render
from .models import LevelPrize, PlayerLevel
from rest_framework import generics, status
import csv
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from .serializers import PlayerLevelSerializer

# Задание №1 Присвоение игроку приза за прохождение уровня.

# Вводные данные уровень. Создаем объект Игрок_Уровень.
# Игрок - авторизованный пользователь.
# Автоматически (по сигналу) меняется поле is_completed на True.
# Автоматически (по сигналу) создается обект Игрок_Приз.
# Приз вытягивается из связанного (заданного аминистратором в админке) объекта Уровень_Приз
class PlayerLevelCreateView(generics.CreateAPIView):
    queryset = PlayerLevel.objects.all()
    serializer_class = PlayerLevelSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        request=PlayerLevelSerializer,
        responses={"201": PlayerLevelSerializer, "400": {"default": "Bad request"}},
        description="Присвоение игроку приза за прохождение уровня",
    )
    def perform_create(self, serializer):
        player = self.request.user
        if player:
            serializer.is_valid(raise_exception=True)
            player_level = serializer.save(player=player)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise AuthenticationFailed("Не прошедший проверку подлинности!")

# Задание №2
# Выгрузку в csv следующих данных: id игрока, название уровня, пройден ли уровень,
# полученный приз за уровень. Учесть, что записей может быть 100 000 и более.

def export_player_levels_to_csv(request):
    # Устанавливаем заголовок ответа для CSV-файла
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="player_levels.csv"'
    
    # Создаем объект для записи в CSV
    writer = csv.writer(response)
    
    # Записываем заголовки столбцов
    writer.writerow(['Игрок ID', 'Уровень', 'Пройден', 'Приз'])

    # Получаем все записи из PlayerLevel
    player_levels = PlayerLevel.objects.all()

    for player_level in player_levels:
        # Получаем уровень
        level = player_level.level
        # Получаем приз, связанный с уровнем
        level_prize = LevelPrize.objects.filter(level=level).first()
        prize = level_prize.prize.title

        # Записываем данные в CSV
        writer.writerow([
            player_level.player.player_id,
            level.title,
            player_level.completed,
            prize
        ])

    return response
