from django.urls import path
from .views import CommentCreateList, CommentOne, CommentOneUpdate


urlpatterns = [
    path('create/', CommentCreateList.as_view()),
    path('one_comment/<str:pk>/', CommentOneUpdate.as_view()),
    path('one_comment/<str:pk>/update_kind/', CommentOne.as_view()),

  
]