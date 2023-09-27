from django.db import models
import uuid
from us.models import Profile
from tic.models import Ticket

class Message(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    STATUS = (
            ('Непрочитано', 'Непрочитано'),
            ('Прочитано', 'Прочитано'),
            )
    body = models.TextField(verbose_name='Текст сообщения')
    kind = models.CharField(max_length=50, choices=STATUS, default='Непрочитано', 
                            blank=True, null=True, verbose_name='Статус сообщения')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    



    def __str__(self):
        return 'Сообщение пользователя {}'.format(self.author.username)

    class Meta:
        ordering = ['kind','-created']
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'