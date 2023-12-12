from django.urls import path
from . views import (
    OrderCreateView, 
    OrdersActivityList,
    OrdersNotActivityList,
    UpdateStatusOrder,
    OrdersListForAdmin,
    OrderOneList,
    UpdateStatusOrder,
    MyNotificationNoReadList,
    OneNotificationNoReadList,
    Order_a_callCreateView,
    Order_a_callActivityList,
    Order_a_callNoActivityList,
    OneOrder_a_callList

    
)

urlpatterns = [
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
    path('create_order_a_call/', Order_a_callCreateView.as_view(), name='create_order_a_call'),
    path('my_orders_a_call_activity/', Order_a_callActivityList.as_view(), name='my_orders_a_call_activity'),
    path('my_orders_a_call_noactivity/', Order_a_callNoActivityList.as_view(), name='my_orders_a_call_noactivity'),
    path('one_order_a_call/<int:pk>/', OneOrder_a_callList.as_view(), name='create_order_a_call'),
    path("notifications/", MyNotificationNoReadList.as_view(), name="notification_list"),
    path("notification/<int:pk>/", OneNotificationNoReadList.as_view(), name="notification"),
    path("my_orders_activity/", OrdersActivityList.as_view(), name="order_list"),
    path("my_orders_not_activity/", OrdersNotActivityList.as_view(), name="history_of_orders_list"),
    path("update_status_order/<int:pk>/", UpdateStatusOrder.as_view(), name="update_status_orders"),
    path("orders/", OrdersListForAdmin.as_view(), name="orders_list_for_admin"),
    path("single_order/<int:pk>/", OrderOneList.as_view(), name="single_order"),


    
] 