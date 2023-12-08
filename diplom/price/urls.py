from django.urls import path
from .views import ProgramListView

urlpatterns = [
    path('', ProgramListView.as_view(), name='prices_list'),    
] 