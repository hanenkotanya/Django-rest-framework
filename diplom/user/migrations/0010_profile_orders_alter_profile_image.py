# Generated by Django 4.2.7 on 2023-11-24 12:50

from django.conf import settings
from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_profile_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='orders',
            field=models.ManyToManyField(blank=True, related_name='my_orders_active', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=user.models.get_avatar_full_path),
        ),
    ]