from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("history", views.Search_HistoryList.as_view(), name="history"),
]
