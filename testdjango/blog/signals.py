from django.db.models.signals import post_delete
from user.models import User
from .models import Post


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        posts = Post.objects.filter(creator=user)
        posts.delete()
    except:
        pass


post_delete.connect(deleteUser, weak=False, sender=User)
