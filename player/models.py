from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Player(AbstractUser):
    player_id = models.UUIDField(default=uuid.uuid4, unique=True, 
                                 primary_key=True, verbose_name="Айди пользователя")
    password = models.CharField(max_length=255, verbose_name="Пароль")
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="Электронная почта"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    username = models.CharField(
        max_length=50, unique=True, verbose_name="Имя пользователя"
    )
    points = models.IntegerField(default=0, verbose_name="Количество баллов")
    first_entrance = models.BooleanField(default=False, verbose_name="Первый вход")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"