
from django.urls import path
from . import views



urlpatterns = [
    path('createMessage/<str:id>/', views.createMessage, name='createMessage'),
    path('editRole/<str:id>/', views.editRole, name='editRoleMessage'),
    path('deleteMessage//<str:id>/<str:slug>/', views.deleteMessage, name='deleteMessage'),

]