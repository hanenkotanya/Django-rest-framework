from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('userProfile/<str:slug>/', views.userProfile, name='userProfile'),
    path('logoutUser/', views.logoutUser, name='logoutUser'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('tickets/', include('tic.urls')),
    


]