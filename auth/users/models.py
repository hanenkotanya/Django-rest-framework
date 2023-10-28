from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify

class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # TODO

    ROLE_CHOICES = (
        ('Пользоваетль', 'Пользоваетль'),
        ('Админ', 'Админ')
    )

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Пользователь')
    slug =  models.SlugField(unique=True, verbose_name='Слаг', blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    intro = models.CharField(max_length=50, blank=True, null=True, verbose_name='Обо мне')
    
    objects = UserManager()

    def  generate_slug(self):
        return slugify(self.username)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args,**kwargs)

        objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    
