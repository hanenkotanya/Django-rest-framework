from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils.text import slugify


class Profile(models.Model):
    ROLE = (
            ('None', 'Обозначьте статус задачи'),
            ('Пользователь', 'Пользователь',),
            ('Соппорт', 'Соппорт')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Юзер')
    role = models.CharField(max_length=50, choices=ROLE, default='b', 
                            blank=True, null=True, verbose_name='Роль')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя')
    email = models.EmailField(max_length=100, blank=True, null=True, 
                              unique=True, verbose_name='Электронная почта')
    slug =  models.SlugField(unique=True, verbose_name='Слаг', blank=True, null=True)
    username = models.CharField(max_length=50, default='Любопытная булочка', blank=True, 
                                null=True, verbose_name='Имя пользователя')
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name='Город')
    intro = models.CharField(max_length=50, blank=True, null=True, verbose_name='Обо мне')
    image = models.ImageField(blank=True, null=True,
                              default='us_images/default.jpg',
                              upload_to='us_images')
    created = models.DateTimeField(auto_now_add=True)
    resolverKind = models.IntegerField(default=0, null=True, blank=True)
    unresolverKind = models.IntegerField(default=0, null=True, blank=True)
    fronzenKind = models.IntegerField(default=0, null=True, blank=True)
    

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)
    
    def  generate_slug(self):
        return slugify(self.user.username)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_slug()
        super().save(*args,**kwargs)


    @property
    def getKindCount(self):
        tickets = self.tickets.all()
        resolverKind = tickets.filter(kind = 'Решенные').count()
        unresolverKind = tickets.filter(kind = 'Нерешенные').count()
        fronzenKind = tickets.filter(kind = 'Замороженные').count()
        
        self.resolverKind = resolverKind
        self.unresolverKind = unresolverKind
        self.fronzenKind = fronzenKind
        self.save()

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
