from django.urls import path
from .views import (
    ProfileUserForAdminSearchView,
    RegisterView, 
    LoginView, 
    UserView, 
    AnimatorsListView, 
    AnimatorsOneListView, 
    ProfileUpdate, 
    ProfileView, 
    ProfileDelete, 
    LogoutView, 
    ProfileUpdateForAnimatorsOrAdministrator
)
from personage.views import PersonageLikeListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserView.as_view(), name = 'user'),
    path('my_profile/', ProfileView.as_view(), name = 'my_profile'),
    path('my_likes/', PersonageLikeListView.as_view(), name = 'my_likes'),
    path(
        'my_profile_update_for_animators_or_administartor/<str:pk>/', 
        ProfileUpdateForAnimatorsOrAdministrator.as_view(),
        name = 'my_profile_update_for_animators_or_administartor'),
    path(
        'my_profile_update/<str:pk>/', ProfileUpdate.as_view(),
        name='my_profile_update'),
    path(
        'my_profile_delete/<str:pk>/', ProfileDelete.as_view(),
        name='my_profile_delete'),
    path('animators/', AnimatorsListView.as_view(), name='animators'),
    path('animator_one/<str:pk>/', AnimatorsOneListView.as_view(), name='animator_one'),
    path('search/', ProfileUserForAdminSearchView.as_view(), name='search'),

]