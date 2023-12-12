from .serializers import (
    ReviewSerializer, 
)
from rest_framework.exceptions import AuthenticationFailed
from user.models import User, Profile
from .models import Review
from order.models import Notification
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]
    @extend_schema(
        request=ReviewSerializer,
        responses={
            "201": ReviewSerializer,
            "400": {"default": "Bad request"}
        },
        description="Создание отзыва" , 
    )
    def perform_create(self, serializer):
        profile = Profile.objects.get(user = self.request.user)
        if profile.role == "Пользователь":
            serializer.is_valid(raise_exception=True)
            serializer.save(from_user = self.request.user)
            message = f"Благодарим за отзыв! Будем ждать вас снова!"
            Notification.objects.create(recipient=self.request.user, message=message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise AuthenticationFailed('Не прошедший проверку подлинности!')
        

@extend_schema_view(get=extend_schema(description="Все отзывы"))    
class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        reviews = Review.objects.all()
        return reviews
