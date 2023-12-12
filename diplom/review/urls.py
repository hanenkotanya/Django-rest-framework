from django.urls import path
from .views import ReviewCreateView, ReviewList

urlpatterns = [
    path('create_review/', ReviewCreateView.as_view(), name='create_review'),  
    path('reviews_list/', ReviewList.as_view(), name='reviews_list'),    
] 