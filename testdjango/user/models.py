from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
import uuid


class User(AbstractUser):
    ROLE_CHOICES = (
        ("Пользователь", "Пользователь"),
        ("Администратор", "Администратор"),
    )
    password = models.CharField(max_length=255, verbose_name="Пароль")
    slug = models.SlugField(unique=True, verbose_name="Слаг", blank=True, null=True)
    email = models.EmailField(
        max_length=255, unique=True, verbose_name="Электронная почта"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    username = models.CharField(
        max_length=50, unique=True, verbose_name="Имя пользователя"
    )
    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default="Пользователь", verbose_name="Роль"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return str(self.username)

    def generate_slug(self):
        return slugify(self.email)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args, **kwargs)

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    full_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Имя пользователя"
    )
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=True
    )

    objects = UserManager()

    def __str__(self):
        return str(self.user)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
