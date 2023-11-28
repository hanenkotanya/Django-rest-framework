from user.models import User
from .models import Order, Notification, Tasks
from celery import shared_task


@shared_task
def create_notice_of_revocation(pk):
    order = Order.objects.filter(pk=pk)
    b = Tasks(order = order)
    message = f"Как прошел заказ? Оставьте пожалуйста отзыв) Ваше мнение очень важно для нас!"
    Notification.objects.create(recipient=order.to_recipient_user, message=message)
    b.save()
