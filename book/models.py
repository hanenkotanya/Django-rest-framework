from django.db import models
from user.models import User


class Book(models.Model):
    STATUS_CHOICES = (
        ("В наличии", "В наличии"),
        ("Выдана", "Выдана"),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",
        verbose_name="Владелец",
    )
    title = models.CharField(
        max_length=50, verbose_name="Название книги"
    )
    author = models.CharField(
        max_length=5000, blank=True, null=True, verbose_name="Автор книги"
    )
    year = models.CharField(
        max_length=5000, blank=True, null=True, verbose_name="Год издания"
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="В наличии",
        verbose_name="Статус книги",
    )

    def __str__(self):
        return str(self.title)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
