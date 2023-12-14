from django.urls import path
from .views import (
    PersonageCreateView, 
    PersonageListView, 
    PersonageOneListView, 
    PersonageOneUpdateView, 
    PersonageOneLikeDeleteView,
    PersonageOneLikeView, 
    PersonageDeleteView, 
    KomboListView,
    PersonageSearchView,
    Life_size_puppetListView
)


urlpatterns = [
    path('create_personage/', PersonageCreateView.as_view(), name='create_personage'),
    path('search/', PersonageSearchView.as_view(), name='search'),
    path('personage_list/', PersonageListView.as_view(), name='personage_list'),
    path('kombo_list/', KomboListView.as_view(), name='kombo_list'),
    path('life_size_puppet_list/', Life_size_puppetListView.as_view(), name='life_size_puppet_list'),
    path('personage_one/<int:pk>/', PersonageOneListView.as_view(), name='personage_one'),
    path('personage_one/<int:pk>/like/', PersonageOneLikeView.as_view(), name='personage_one_like'),
    path('personage_one/<int:pk>/like_delete/', PersonageOneLikeDeleteView.as_view(), name='personage_one_like_delete'),
    path('personage_one_update/<int:pk>/', PersonageOneUpdateView.as_view(), name='personage_one_update'),
    path('personage_one_delete/<int:pk>/', PersonageDeleteView.as_view(), name='personage_one_delete'),


] 