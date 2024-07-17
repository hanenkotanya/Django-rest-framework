from django.db import models
from user.models import User


class City(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название города")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"


class Search_History(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default="",
        blank=True,
        null=True,
        verbose_name="Название города",
    )
    name_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        default="",
        blank=True,
        null=True,
        verbose_name="Название города",
    )
    date = models.DateTimeField(
        verbose_name="Дата и время поиска",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Попытка поиска города"
        verbose_name_plural = "История поиска"
