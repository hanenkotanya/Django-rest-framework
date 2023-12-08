from .serializers import (
    OrderSerializer, 
    NotificationSerializer, 
    UpdateOrderSerializer, 
    NotificationSerializeRead,
    Order_a_callSerializer
)
from rest_framework.exceptions import AuthenticationFailed
from user.models import User, Profile
from .models import Order, Notification, Order_a_call
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from personage.permissions import IsOnlyAdministrator, IsOnlyAnimator
from user.permissions import IsOnlyAdministratorOrAnimators
from django.dispatch import receiver
from .models import Order
from order.tasks import create_notice_of_revocation
from rest_framework.generics import get_object_or_404



class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, ]
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
        

@extend_schema_view(get=extend_schema(
    description="Все активные заказы для текущего пользователя или аниматора"
    ))
class OrdersActivityList(generics.ListAPIView):
    queryset = Order.objects.filter(activity = True)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        orders = Order.objects.filter(
        Q(activity = True)
        & (Q(to_recipient_user=self.request.user)
        | Q(to_recipient_animators=self.request.user))
        )
        return orders
    

@extend_schema_view(get=extend_schema(description="Заказ"))
class OrderOneList(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        order = Order.objects.filter(
            Q(pk=pk)
            & (Q(to_recipient_user=self.request.user)
            | Q(to_recipient_animators=self.request.user))
        )
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)



@extend_schema_view(get=extend_schema(
    description="Все прошедшие заказы для текущего пользователя или аниматора"
    ))
class OrdersNotActivityList(generics.ListAPIView):
    queryset = Order.objects.filter(activity = False)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        orders = Order.objects.filter(
        Q(activity = False)
        & (Q(to_recipient_user=self.request.user)
        | Q(to_recipient_animators=self.request.user))
        )
        return orders



@extend_schema_view(get=extend_schema(description="Все заказы для админа"))    
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
    permission_classes = [IsAuthenticated, IsOnlyAdministratorOrAnimators]
    @extend_schema(
        request=UpdateOrderSerializer,
        responses={
            "201": UpdateOrderSerializer,
            "400": {"default": "Bad request"}
        },
        description="Обновление статуса заказа аниматором или администратором" , 
    )
    def change_activity(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = self.serializer_class(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        create_notice_of_revocation.delay(order.pk)
        serializer.save()
        return Response(serializer.data)
    

@extend_schema_view(get=extend_schema(description="Все активные уведомления для текущего пользователя"))
class MyNotificationNoReadList(generics.ListAPIView):
    queryset = Notification.objects.filter(read = False)
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        notifications = Notification.objects.filter(
        Q(read = False)
        & (Q(recipient=self.request.user))
        )
        return notifications
    

@extend_schema_view(get=extend_schema(description="Уведомление для текущего пользователя"))
class OneNotificationNoReadList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializeRead
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    def get(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class Order_a_callCreateView(generics.CreateAPIView):
    queryset = Order_a_call.objects.all()
    serializer_class = Order_a_callSerializer
    permission_classes = [IsAuthenticated, ]
    @extend_schema(
        request=Order_a_callSerializer,
        responses={
            "201": Order_a_callSerializer,
            "400": {"default": "Bad request"}
        },
        description="Создание заказа звонка администратора" , 
    )
    def perform_create(self, serializer):
        profile_user = Profile.objects.get(user = self.request.user)
        if profile_user.role == "Пользователь":
            serializer.is_valid(raise_exception=True)
            recipient = Profile.objects.get(role="Администратор")
            
            serializer.save(from_creator_user = self.request.user, 
                                            recipient = recipient.user,
                                            phone_number=profile_user.phone_number)
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        else:
            raise AuthenticationFailed('Не прошедший проверку подлинности!')
        

@extend_schema_view(get=extend_schema(
    description="Все активные заказы звонка для Администратора"
    ))
class Order_a_callActivityList(generics.ListAPIView):
    queryset = Order_a_call.objects.filter(read = False)
    serializer_class = Order_a_callSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    def get_queryset(self):
        orders_a_call = Order_a_call.objects.filter(
        Q(read = False)
        & (Q(recipient=self.request.user)
        ))
        return orders_a_call


@extend_schema_view(get=extend_schema(description="Активный запрос на звонок для администратора"))
class OneOrder_a_callNoReadList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order_a_call.objects.all()
    serializer_class = NotificationSerializeRead
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageNumberPagination
    def get(self, request, pk):
        order_a_call = get_object_or_404(Order_a_call, pk=pk)
        serializer = Order_a_callSerializer(order_a_call)
        return Response(serializer.data)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)       

    




