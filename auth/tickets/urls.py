from django.urls import path, include
from .views import TicketCreateList, TicketList, TicketOneUpdate, TicketDelete

urlpatterns = [
    path('ticket/<str:pk>/comments/', include('comments.urls')),
    path('create/', TicketCreateList.as_view()),
    path('mytickets/', TicketCreateList.as_view()),
    path('tickets_for_sopport/', TicketList.as_view()),
    path('ticket/<str:pk>/', TicketOneUpdate.as_view()),
    path('ticket/<str:pk>/update_role/', TicketOneUpdate.as_view()),
    path('ticket/<str:pk>/delete/', TicketDelete.as_view()),

   
]