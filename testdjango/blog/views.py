from .serializers import (
    PostSerializer,
    UpdatePostSerializer,
)
from .models import Post
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsOnlyMyPostOrAdmin
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from django.http import response


class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    @extend_schema(
        request=PostSerializer,
        responses={"201": PostSerializer, "400": {"default": "Bad request"}},
        description="Создание поста",
    )
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(creator=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(description="Все активные посты для текущего пользователя")
)
class MyPostsActivityList(generics.ListAPIView):
    queryset = Post.objects.filter(activity=True)
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        posts = Post.objects.filter(Q(activity=True) & (Q(creator=self.request.user)))
        return posts


@extend_schema_view(get=extend_schema(description="Все активные посты"))
class PostsActivityList(generics.ListAPIView):
    queryset = Post.objects.filter(activity=True)
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        posts = Post.objects.filter(activity=True)
        return posts


@extend_schema_view(get=extend_schema(description="Пост"))
class PostOneList(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get(self, request, pk):
        order = Post.objects.filter(pk=pk)
        serializer = PostSerializer(order, many=True)
        return Response(serializer.data)


@extend_schema_view(
    get=extend_schema(
        description="Все неопубликованные посты для текущего пользователя"
    )
)
class MyPostsNotActivityList(generics.ListAPIView):
    queryset = Post.objects.filter(activity=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        orders = Post.objects.filter(Q(activity=False) & (Q(creator=self.request.user)))
        return orders


class UpdatePost(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer
    permission_classes = [IsAuthenticated, IsOnlyMyPostOrAdmin]

    @extend_schema(
        request=UpdatePostSerializer,
        responses={"201": UpdatePostSerializer, "400": {"default": "Bad request"}},
        description="Изменение поста автором или администратором",
    )
    def change_activity(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = self.serializer_class(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOnlyMyPostOrAdmin]

    @extend_schema(
        request=PostSerializer,
        responses={
            204: None,
            400: {"default": "Bad request"},
            404: {"default": "Not found."},
        },
        description="Удаление поста автором или администратором",
    )
    def delete_post(self, request, pk):
        post = Post.objects.filter(pk=pk)
        post.delete()
        response.data = {"message": "Успешно"}
        return response
