from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, Notification
from .tasks import create_notice_of_revocation
from .views import UpdateStatusOrder

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    if instance.status == "Успешно": 
        create_notice_of_revocation.delay(instance.pk)



post_save.connect(UpdateStatusOrder, sender=Notification)


