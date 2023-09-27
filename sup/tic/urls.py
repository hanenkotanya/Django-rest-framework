from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('createTickets/<str:slug>/', views.createTicket, name='createTickets'),
    path('userTickets/<str:slug>/', views.userTickets, name='userTickets'),
    path('tickets-all/', views.tickets, name='ticketsAll'),
    path('messages/', include('mes.urls')),
    path('ticketThis/<str:id>/', views.ticketThis, name='ticketThis'),
    path('deleteTicket/<str:id>/<str:slug>/', views.deleteTicket, name='deleteTicket'),
    path('editRole/<str:id>/', views.editRole, name='editRole'),
    
]