from django.db import models
import uuid
from users.models import User


class Ticket(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    STATUS = (
            ('None', 'Обозначьте статус задачи'),
            ('Нерешенные', 'Нерешенные'),
            ('Решенные', 'Решенные'),
            ('Замороженные', 'Замороженные'),
            )
    subject = models.CharField(max_length=200, blank=True, null=True, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст обращения')
    kind = models.CharField(max_length=50, choices=STATUS, default='Нерешенные', 
                            blank=True, null=True, verbose_name='Тип объявления')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    


    def __str__(self):
        return 'Тикет пользователя {}'.format(self.author.username)

    class Meta:
        ordering = ['kind','-created']
        verbose_name = 'Тикет'
        verbose_name_plural = 'Тикеты'

