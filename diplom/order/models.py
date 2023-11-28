from django.db import models
from user.models import User
from personage.models import Personage, Kombo
from rest_framework.exceptions import ValidationError



class Order(models.Model):
    ROLE_CHOICES = (
        ('В ожидании', 'В ожидании'),
        ('Успешно', 'Успешно'),
        ('Отмена', 'Отмена'),
    )
    from_creator_administrator = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, related_name = 'orders', verbose_name='Создатель')
    to_recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_orders',  verbose_name='Заказ пользователя')
    to_recipient_animators = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'animator_orders', verbose_name='Заказ на аниматора')
    personage = models.ForeignKey(Personage, blank=True, null=True, on_delete=models.CASCADE, related_name = 'orders', verbose_name='Персонаж')
    kombo = models.ForeignKey(Kombo, blank=True, null=True, on_delete=models.CASCADE, related_name = 'orders', verbose_name='Комбо')
    notes = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Примечания')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    activity = models. BooleanField(default=True, verbose_name='Активность')
    changes = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.CharField(max_length=50, choices=ROLE_CHOICES, default='В ожидании')
    data_time_order =models.DateTimeField(verbose_name='Дата и время заказа')
    sale = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return str(f'Заказ пользователя {self.to_recipient_user}')
    
    def clean(self):
        if self.from_creator_administrator == self.to_recipient_user or self.from_creator_administrator == self.to_recipient_animators:
            raise ValidationError("Users cannot friend themselves.")

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

    def reject(self):
        self.delete()

    def accept(self):
        self.from_creator_administrator.profile.orders.add(self.order)
        self.to_recipient_user.profile.orders.add(self.order)
        self.to_recipient_animators.profile.orders.add(self.order)
        self.delete()

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Notification(models.Model):
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_notifications"
    )  # получатель уведомления
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    message = models.CharField(max_length=255, default="")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return str(f'Уведомление для пользователя {self.recipient.username}')
    

class Tasks(models.Model):
    task_id = models.CharField(max_length=50)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.task_id}'