# Generated by Django 4.2.7 on 2023-11-11 13:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('personage', '0004_alter_personage_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personage',
            name='creator',
        ),
        migrations.AddField(
            model_name='personage',
            name='creator',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
    ]