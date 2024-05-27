from django.urls import path
from .views import (
    PostCreateView,
    MyPostsActivityList,
    MyPostsNotActivityList,
    PostsActivityList,
    UpdatePost,
    PostOneList,
    PostDeleteView,
)

urlpatterns = [
    path("create_post/", PostCreateView.as_view(), name="create_post"),
    path("my_posts_activity/", MyPostsActivityList.as_view(), name="posts_list"),
    path(
        "my_posts_not_activity/",
        MyPostsNotActivityList.as_view(),
        name="posts_not_activity_list",
    ),
    path("update_post/<int:pk>/", UpdatePost.as_view(), name="update_post"),
    path("posts/", PostsActivityList.as_view(), name="posts_list"),
    path("single_post/<int:pk>/", PostOneList.as_view(), name="single_post"),
    path("post_delete/<int:pk>/", PostDeleteView.as_view(), name="delete_post"),
]
