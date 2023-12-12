from django.db import models
from user.models import User, Profile
from personage.models import Personage, Kombo
from price.models import Program
from rest_framework.exceptions import ValidationError



class Order(models.Model):
    ROLE_CHOICES = (
        ('В ожидании', 'В ожидании'),
        ('Успешно', 'Успешно'),
        ('Отмена', 'Отмена'),
    )
    from_creator_administrator = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, related_name = 'orders', verbose_name='Создатель')
    to_recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'user_orders',  verbose_name='Заказ пользователя')
    to_recipient_animators = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = 'animator_orders', verbose_name='Заказ на аниматора')
    to_recipient_two_animators = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = 'animator_two_orders', verbose_name='Заказ на второго аниматора')
    to_recipient_three_animators = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name = 'animator_three_orders', verbose_name='Заказ на третьего аниматора')
    personage = models.ForeignKey(Personage, blank=True, null=True, on_delete=models.CASCADE, related_name = 'orders', verbose_name='Персонаж')
    personage_two = models.ForeignKey(Personage, blank=True, null=True, on_delete=models.CASCADE, related_name = 'orders_for_two', verbose_name='Второй персонаж')
    personage_three = models.ForeignKey(Personage, blank=True, null=True, on_delete=models.CASCADE, related_name = 'orders_for_three', verbose_name='Третий персонаж')
    kombo = models.ForeignKey(Kombo, blank=True, null=True, on_delete=models.CASCADE, related_name = 'orders', verbose_name='Комбо')
    notes = models.CharField(max_length=5000, blank=True, null=True, verbose_name='Примечания')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    activity = models. BooleanField(default=True, verbose_name='Активность')
    changes = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    status = models.CharField(max_length=50, choices=ROLE_CHOICES, default='В ожидании')
    data_time_order =models.DateTimeField(verbose_name='Дата и время заказа')
    sale = models.IntegerField(blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True, related_name = 'program',  verbose_name='Программа')

    def __str__(self):
        return str(f'Заказ пользователя {self.to_recipient_user}')
    
    def clean(self):
        if self.from_creator_administrator == self.to_recipient_user or self.from_creator_administrator == self.to_recipient_animators:
            raise ValidationError("Users cannot friend themselves.")

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

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
    

class Order_a_call(Notification):
    TIME_CHOICES = (
        ('В течении получаса', 'В течении получаса'),
        ('Через один час', 'Через один час'),
        ('Через два часа', 'Через два часа'),
    )

    from_creator_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="get_order_a_call"
    )  # отправитель зaказа на звонок
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    time_to_call = models.CharField(max_length=50, choices=TIME_CHOICES, 
                                   default='В течении получаса',  verbose_name = "Желаемое время звонка")
    info_for_users = models.CharField(max_length=50, default='Администратор может вам набрать с 9.00 да 18.00')
