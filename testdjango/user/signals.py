from django.db.models.signals import post_save, post_delete
from .models import User
from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(user=user, full_name=user.username)


def updateProfile(sender, instance, created, **kwargs):
    user = instance.user
    profile = Profile.objects.get(user=user)
    user.username = profile.full_name
    user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, weak=False, sender=User)
post_save.connect(updateProfile, weak=False, sender=Profile)
post_delete.connect(deleteUser, weak=False, sender=Profile)
