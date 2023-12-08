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
)

urlpatterns = [
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
    path("notifications/", MyNotificationNoReadList.as_view(), name="notification_list"),
    path("notification/<int:pk>/", OneNotificationNoReadList.as_view(), name="notification"),
    path("my_orders_activity/", OrdersActivityList.as_view(), name="order_list"),
    path("my_orders_not_activity/", OrdersNotActivityList.as_view(), name="history_of_orders_list"),
    path("update_status_order/<int:pk>/", UpdateStatusOrder.as_view(), name="update_status_orders"),
    path("orders/", OrdersListForAdmin.as_view(), name="orders_list_for_admin"),
    path("single_order/<int:pk>/", OrderOneList.as_view(), name="single_order"),
    path("orders/", MyNotificationNoReadList.as_view(), name="orders_list_for_admin"),

    
] 