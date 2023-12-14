from django.db import models


class Program(models.Model):
    PRICE_CHOICES = (
        ('choises', 'choises'),
        ('150 руб', '150 руб'),
        ('210 руб', '210 руб'),
        ('330 руб', '330 руб'),
        ('430 руб', '430 руб'),

    )
    TIME_CHOICES = (
        ('choises', 'choises'),
        ('60 минут', '60 минут'),
        ('90 минут', '90 минут'),


    )
    name = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Название')
    price = models.CharField(max_length=50, choices=PRICE_CHOICES, default='choises', verbose_name='Выбор цены')
    time = models.CharField(max_length=50, choices=TIME_CHOICES, default='choises', verbose_name='Выбор времени')
    description = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Описание')
    

    class Meta:
        verbose_name = "Программа"
        verbose_name_plural = "Программы"
    
    def __str__(self):
        return str(self.name)

