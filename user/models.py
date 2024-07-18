from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    password = models.CharField(max_length=255, verbose_name="Пароль")
    slug = models.SlugField(unique=True, verbose_name="Слаг", blank=True, null=True)
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

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
