from django.urls import path
from .views import (
    ProfileUserForAdminSearchView,
    RegisterView,
    LoginView,
    UserView,
    ProfileUpdate,
    ProfileView,
    ProfileDelete,
    LogoutView,
    UsersView,
)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("user/", UserView.as_view(), name="user"),
    path("users/", UsersView.as_view(), name="users"),
    path("my_profile/", ProfileView.as_view(), name="my_profile"),
    path(
        "my_profile_update/<str:pk>/", ProfileUpdate.as_view(), name="my_profile_update"
    ),
    path(
        "my_profile_delete/<str:pk>/", ProfileDelete.as_view(), name="my_profile_delete"
    ),
    path("search/", ProfileUserForAdminSearchView.as_view(), name="search"),
]
