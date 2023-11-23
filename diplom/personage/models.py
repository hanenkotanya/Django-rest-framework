from django.db import models
from user.models import User



class Personage(models.Model):
    creator = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, blank=True, verbose_name='Создатель')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    description = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True,
                              default='personage_images/default.jpg',
                              upload_to='personage_images', verbose_name='Фото')
    activity = models. BooleanField(default=True, verbose_name='Активность')
    life_size_puppet = models. BooleanField(default=False, verbose_name='Ростовая кукла')
    


    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Kombo(models.Model):
    personage1=models.ManyToManyField('personage.Personage', related_name ='personagekombo1', blank=True, verbose_name='Первый персонаж')
    personage2=models.ManyToManyField('personage.Personage', related_name ='personagekombo2', blank=True, verbose_name='Второй персонаж')
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя')
    description = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(blank=True, null=True,
                              default='personage_images/default.jpg',
                              upload_to='personage_images', verbose_name='Фото')
    activity = models. BooleanField(default=True, verbose_name='Активность')
    life_size_puppet = models. BooleanField(default=False, verbose_name='Ростовая кукла')
    


    def __str__(self):
        return str(self.name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
