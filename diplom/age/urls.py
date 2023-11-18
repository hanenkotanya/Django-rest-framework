from django.urls import path
from .views import PersonageFor1_4ListView, PersonageFor5_9ListView, PersonageFor10_14ListView

urlpatterns = [
    path('1_4/', PersonageFor1_4ListView.as_view()),
    path('5_9/', PersonageFor5_9ListView.as_view()),
    path('10_14/', PersonageFor10_14ListView.as_view())
    
] 