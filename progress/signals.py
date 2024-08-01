from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PlayerLevel, PlayerPrize, LevelPrize


def createPlayerPrize(sender, instance, created, **kwargs):
    if created:
        level = instance.level
        level_prize = LevelPrize.objects.get(level=level)
        player = instance.player
        player_prize = PlayerPrize.objects.create(
            player=player,
            prize=level_prize.prize     
        )




post_save.connect(createPlayerPrize, sender=PlayerLevel)
