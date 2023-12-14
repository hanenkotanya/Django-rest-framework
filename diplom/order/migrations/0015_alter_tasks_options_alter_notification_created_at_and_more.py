# Generated by Django 4.2.7 on 2023-12-14 10:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0014_order_personage_three_order_personage_two'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tasks',
            options={'verbose_name': 'Задача на создание уведомления о отзыве', 'verbose_name_plural': 'Задачи на создание уведомлений о отзывах'},
        ),
        migrations.AlterField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания уведомления'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(default='', max_length=255, verbose_name='Сообщение'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.BooleanField(default=False, verbose_name='Прочитано'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_notifications', to=settings.AUTH_USER_MODEL, verbose_name='Получатель уведомления'),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sale',
            field=models.IntegerField(blank=True, null=True, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='order_a_call',
            name='from_creator_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_order_a_call', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель зaказа на звонок'),
        ),
        migrations.AlterField(
            model_name='order_a_call',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Телефонный номер'),
        ),
    ]