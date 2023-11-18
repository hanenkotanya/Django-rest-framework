from django.urls import path
from .views import PersonageCreateView, PersonageListView, PersonageOneListView, PersonageOneUpdateView, PersonageOneLikeDeleteView
from .views import PersonageOneLikeView, PersonageDeleteView 

urlpatterns = [
    path('create_personage/', PersonageCreateView.as_view(), name='create_personage'),
    path('personage_list/', PersonageListView.as_view()),
    path('personage_one/<int:pk>/', PersonageOneListView.as_view()),
    path('personage_one/<int:pk>/like/', PersonageOneLikeView.as_view()),
    path('personage_one/<int:pk>/like_delete/', PersonageOneLikeDeleteView.as_view()),
    path('personage_one_update/<int:pk>/', PersonageOneUpdateView.as_view()),
    path('personage_one_delete/<int:pk>/', PersonageDeleteView.as_view()),


] 