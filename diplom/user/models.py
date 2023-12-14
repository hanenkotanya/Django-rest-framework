from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
import uuid
from django.core.validators import RegexValidator


class User(AbstractUser):
    password = models.CharField(max_length=255, verbose_name='Пароль')
    slug =  models.SlugField(unique=True, verbose_name='Слаг', blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, verbose_name='Электронная почта')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    username = models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] #TODO

    def __str__(self):
        return str(self.username)

    def  generate_slug(self):
        return slugify(self.email)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args,**kwargs)
        
    
    objects = UserManager()


def get_avatar_full_path(instance, filename):
    return f"{instance.id}/image/{filename}"


def get_avatar_url(instance, filename):
    return f"https://protfo.pro/{instance.id}/image"


class Profile(models.Model):
    ROLE_CHOICES = (
        ('Пользователь', 'Пользователь'),
        ('Администратор', 'Администратор'),
        ('Аниматор', 'Аниматор')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    full_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя пользователя')
    phone_number = models.CharField(
        max_length=12, blank=True, null=True, verbose_name='Телефонный номер',
        validators=[RegexValidator(regex='^\+?7[-. ]?\d{5,12}$', message='Некорректный формат телефона')])
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Пользователь', verbose_name='Роль')
    intro = models.CharField(max_length=500, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to=get_avatar_full_path, null=True, blank=True, verbose_name='Изображение')
    tiktok = models.CharField(max_length=100, blank=True, null=True, verbose_name='Тикток')
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name='Инстаграм')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    my_likes = models.ManyToManyField(
        'personage.Personage', symmetrical = False, 
        blank=True, related_name ='who_liked', verbose_name='Мои лайки')
    orders = models.ManyToManyField(User, blank=True, related_name="my_orders", verbose_name='Мои заказы')
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

