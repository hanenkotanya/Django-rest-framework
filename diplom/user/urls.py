from django.urls import path
from .views import RegisterView, LoginView, UserView, ProfileUpdate, ProfileView, ProfileDelete, LogoutView, ProfileUpdateForAnimatorsOrAdministrator
from personage.views import PersonageLikeListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view()),
    path('my_profile/', ProfileView.as_view()),
    path('my_likes/', PersonageLikeListView.as_view()),
    path('my_profile_update_for_animators_or_administartor/<str:pk>/', ProfileUpdateForAnimatorsOrAdministrator.as_view()),
    path('my_profile_update/<str:pk>/', ProfileUpdate.as_view()),
    path('my_profile_delete/<str:pk>/', ProfileDelete.as_view()),

]