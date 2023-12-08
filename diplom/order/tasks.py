from user.models import User
from .models import Order, Notification, Tasks
from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task
def create_notice_of_revocation(order_pk):
    print("Start executing create_notice_of_revocation task")
    order = Order.objects.get(pk=order_pk)
    b = Tasks(order=order)
    message = f"Как прошел заказ? Оставьте пожалуйста отзыв) Ваше мнение очень важно для нас!"
    Notification.objects.create(recipient=order.to_recipient_user, message=message)
    b.save()
    print("create_notice_of_revocation task successfully executed")


