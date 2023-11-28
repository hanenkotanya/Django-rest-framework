# Generated by Django 4.2.7 on 2023-11-24 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, max_length=5000, null=True, verbose_name='Примечания')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Дата создания')),
                ('activity', models.BooleanField(default=True, verbose_name='Активность')),
                ('changes', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('data_time_order', models.DateTimeField(verbose_name='Дата и время заказа')),
                ('from_creator_administrator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Создатель')),
                ('to_recipient_animators', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aniator_orders', to=settings.AUTH_USER_MODEL, verbose_name='Заказ на аниматора')),
                ('to_recipient_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL, verbose_name='Заказ пользователя')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
                ('message', models.CharField(default='', max_length=255)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Уведомление',
                'verbose_name_plural': 'Уведомления',
                'ordering': ('-created_at',),
            },
        ),
    ]