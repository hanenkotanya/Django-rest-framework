from django.db import models
from personage.models import Personage, Kombo
from user.models import User


class Review(models.Model):
    from_user = models.ForeignKey(User, on_delete= models.SET_NULL, blank=True, null=True, related_name = 'from_user', verbose_name='Пользователь')
    personage = models.ForeignKey(Personage, on_delete= models.SET_NULL, blank=True, null=True, related_name = 'personage', verbose_name='Персонаж')
    kombo = models.ForeignKey(Kombo, on_delete=models.SET_NULL, blank=True, null=True, related_name = 'kombo',  verbose_name='Kombo')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    description = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Описание')
  
    def __str__(self):
        return str(f'Отзыв пользователя {self.from_user.username}')

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"



