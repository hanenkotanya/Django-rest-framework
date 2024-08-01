from django.urls import path
from . import views
from .views import PlayerLevelCreateView

urlpatterns = [
    path('export_to_csv/', views.export_player_levels_to_csv,),
    path('level_prize/', PlayerLevelCreateView.as_view(), name='LevelPrizeCreateView'),
]

