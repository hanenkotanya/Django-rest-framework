from django.urls import path
from .views import RegisterView, LoginView, UserView, Logout, UserOneUpdate

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', Logout.as_view()),
    path('user_update/<int:pk>/', UserOneUpdate.as_view()),
    path('user_delete/<int:pk>/', UserOneUpdate.as_view()),

]
