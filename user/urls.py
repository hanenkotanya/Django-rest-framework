from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    UserView,  
    UserDelete, 
    LogoutView
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name = 'user'),
    path(
        'user_delete/<str:pk>/', UserDelete.as_view(),
        name='user_delete'),

]