from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager



class User(AbstractUser):
    password = models.CharField(max_length=255, verbose_name="Пароль")
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="Электронная почта"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    username = models.CharField(
        max_length=50, unique=True, verbose_name="Имя пользователя"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  

    def __str__(self):
        return str(self.username)

    objects = UserManager()
