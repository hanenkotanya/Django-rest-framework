# Generated by Django 4.2.4 on 2023-10-27 19:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tickets', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('body', models.TextField(verbose_name='Текст комментария')),
                ('kind', models.CharField(blank=True, choices=[('Непрочитано', 'Непрочитано'), ('Прочитано', 'Прочитано')], default='Непрочитано', max_length=50, null=True, verbose_name='Тип объявления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tickets.ticket')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['kind', '-created'],
            },
        ),
    ]
