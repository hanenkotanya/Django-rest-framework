from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.text import slugify
import uuid
from django.core.validators import RegexValidator


class User(AbstractUser):
    password = models.CharField(max_length=255)
    slug =  models.SlugField(unique=True, verbose_name='Слаг', blank=True, null=True)
    email = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] #TODO

    def  generate_slug(self):
        return slugify(self.email)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args,**kwargs)
    
    objects = UserManager()



class Profile(models.Model):
    ROLE_CHOICES = (
        ('Пользователь', 'Пользователь'),
        ('Администратор', 'Администратор'),
        ('Аниматор', 'Аниматор')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True, validators=[RegexValidator(regex='^\+?7[-. ]?\d{5,12}$', message='Некорректный формат телефона')])
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Пользователь')
    intro = models.CharField(max_length=500, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True,
                              default='profile_images/default.jpg',
                              upload_to='profile_images')
    tiktok = models.CharField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=100, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    my_likes = models.ManyToManyField('personage.Personage', symmetrical = False, blank=True, related_name ='who_liked')

    objects = UserManager()

    def __str__(self):
        return str(self.user)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
