from django.db import models
from player.models import Player

class Boost(models.Model):
    TYPE_CHOICES = (
        ("Нескольких типов бустов", "Нескольких типов бустов"),
        ("type1", "type1"),
        ("type2", "type2"),
        ("type3", "type3"),
    )
    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        default="Нескольких типов бустов",
        verbose_name="Тип буста",
    )
    player = models.ManyToManyField(Player, related_name="boots", verbose_name="Игроки")

    class Meta:
        verbose_name = "Бутс"
        verbose_name_plural = "Бутсы"


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Уровень"
        verbose_name_plural = "Уровни"
    
    
    
class Prize(models.Model):
    title = models.CharField(max_length=100)


    def __str__(self):
        return str(self.title)
    
    class Meta:
        verbose_name = "Приз"
        verbose_name_plural = "Призы"


class MyModelManager(models.Manager):
    def create(self, *args, **kwargs):
        kwargs['is_completed'] = True  # Устанавливаем is_active по умолчанию на True
        return super().create(*args, **kwargs)

    
class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, related_name="playerlevels", on_delete=models.CASCADE)
    level = models.ForeignKey(Level, related_name="playerslevel", on_delete=models.CASCADE)
    completed = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.player.username} - {self.level.title}'
    
    objects = MyModelManager()
    
    class Meta:
        verbose_name = "Игрок-Уровень"
        verbose_name_plural = "Общая таблица связей игрок-уровень"
    
    
class LevelPrize(models.Model):
    level = models.ForeignKey(Level, related_name="levelprize", on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, related_name="levelprize", on_delete=models.CASCADE)
    received = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.level.title} - {self.prize.title}'
    
    class Meta:
        verbose_name = "Уровень-Приз"
        verbose_name_plural = "Общая таблица связей уровень-приз"


class PlayerPrize(models.Model):
    player = models.ForeignKey(Player, related_name="playerprize", on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, related_name="playerprize", on_delete=models.CASCADE)
    received = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'{self.player.username} - {self.prize.title}'
    
    class Meta:
        verbose_name = "Игрок-Приз"
        verbose_name_plural = "Общая таблица связей игрок-приз"


