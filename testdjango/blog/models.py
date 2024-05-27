from django.db import models
from user.models import User



class Post(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name="Создатель",
    )
    name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Имя поста"
    )
    text = models.CharField(
        max_length=5000, blank=True, null=True, verbose_name="Текст поста"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    activity = models.BooleanField(default=True, verbose_name="Опубликовано")
    changes = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return str(f"Пост пользователя {self.creator}")

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
