from django.contrib import admin
from .models import PlayerLevel, Prize, Level, LevelPrize, PlayerPrize

admin.site.register(PlayerLevel)
admin.site.register(Prize)
admin.site.register(Level)
admin.site.register(LevelPrize)
admin.site.register(PlayerPrize)

