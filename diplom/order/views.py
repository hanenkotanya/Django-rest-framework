from .serializers import OrderSerializer, NotificationSerializer, UpdateOrderSerializer
from rest_framework.exceptions import AuthenticationFailed
from user.models import User, Profile
from .models import Order, Notification
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from personage.permissions import IsOnlyAdministrator, IsOnlyAnimator
from django.dispatch import receiver
from .models import Order
from order.tasks import create_notice_of_revocation




class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated,  ]
    @extend_schema(
        request=OrderSerializer,
        responses={
            "201": OrderSerializer,
            "400": {"default": "Bad request"}
        },
        description="Создание заказа администратором" , 
    )
    def perform_create(self, serializer):
        profile = Profile.objects.get(user = self.request.user)
        if profile.role == "Администратор":
            serializer.is_valid(raise_exception=True)
            order_request = serializer.save(from_creator_administrator = self.request.user)
            message = f"Вам пришел заказ от {self.request.user.username}."
            Notification.objects.create(recipient=order_request.to_recipient_user, message=message)
            Notification.objects.create(recipient=order_request.to_recipient_animators, message=message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise AuthenticationFailed('Не прошедший проверку подлинности!')
        
@extend_schema_view(get=extend_schema(description="Все активные заказы для текущего пользователя"))
class OrdersActivityList(generics.ListAPIView):
    queryset = Order.objects.filter(activity = True)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        orders = Order.objects.filter(
        Q(activity = True)
        & (Q(to_recipient_user=self.request.user)
        | Q(to_recipient_user=self.request.user))
        )
        return orders
    

@extend_schema_view(get=extend_schema(description="Заказ"))
class OrderOneList(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        order = Order.objects.filter(pk=pk)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)



@extend_schema_view(get=extend_schema(description="Все прошедшие заказы для текущего пользователя"))
class OrdersNotActivityList(generics.ListAPIView):
    queryset = Order.objects.filter(activity = False)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        orders = Order.objects.filter(
        Q(activity = False)
        & (Q(to_recipient_user=self.request.user)
        | Q(to_recipient_user=self.request.user))
        )
        return orders


@extend_schema_view(get=extend_schema(description="Все уведомления для текущего пользователя"))
class NotificationList(generics.ListCreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
    
class OrdersListForAdmin(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOnlyAdministrator]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        orders = Order.objects.all()

        return orders


class UpdateStatusOrder(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = UpdateOrderSerializer
    permission_classes = [IsAuthenticated, IsOnlyAnimator]
    def change_activity(self, request, pk):
        order = Order.objects.filter(pk=pk)
        serializer_data = request.data.get(order)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        create_notice_of_revocation.delay(order.pk)
        serializer.save()
        return Response (serializer.data)





