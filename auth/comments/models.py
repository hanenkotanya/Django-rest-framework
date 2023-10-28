from django.db import models
import uuid
from users.models import User
from tickets.models import Ticket


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    STATUS = (
            ('Непрочитано', 'Непрочитано'),
            ('Прочитано', 'Прочитано'),
            )
    body = models.TextField(verbose_name='Текст комментария')
    kind = models.CharField(max_length=50, choices=STATUS, default='Непрочитано', 
                            blank=True, null=True, verbose_name='Тип объявления')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=True)
    


    def __str__(self):
        return 'Комментария пользователя {}'.format(self.author.username)

    class Meta:
        ordering = ['kind','-created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
