from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from rest_framework import generics
from .models import Ticket
from comments.models import Comment
from . import serializers
from rest_framework import generics
from .permissions import IsAdminOrReadOnlyForAuthor, IsOnlyAdmin, IsOnlyAuthor
import jwt
from rest_framework.exceptions import AuthenticationFailed

def get_user(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Не прошедший проверку подлинности!')
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Не прошедший проверку подлинности!')
    user = User.objects.filter(id=payload['id']).first()
    return user


class TicketCreateList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketsSerializer
    def perform_create(self, serializer):
        serializer.save(author = get_user(self.request))
    def get(self, request):
        tickets = Ticket.objects.alias().filter(author = get_user(self.request))    
        serializer = serializers.TicketsSerializer(tickets, many=True)
        return Response(serializer.data)
    
class TicketList(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketsSerializer
    permission_classes = [IsOnlyAdmin]
    def get_for_soport(self, request):
        tickets = Ticket.objects.all()  
        self.check_object_permissions(self.request, tickets)
        serializer = serializers.TicketsSerializer(tickets, many=True)
        return Response(serializer.data)

               
class TicketOneUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketsSerializerUpdateKind
    permission_classes = [IsAdminOrReadOnlyForAuthor]
    def get_one_ticket(self, requets, pk):
        ticket = Ticket.objects.filter(pk=pk) 
        serializer = serializers.TicketsSerializer(ticket, many=True)
        return Response(serializer.data)

    def update_kind(self, request, pk):
        ticket = Ticket.objects.filter(pk=pk)  
        serializer_data = request.data.get(ticket)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)
    
class TicketDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketsSerializerUpdateKind
    permission_classes = [IsOnlyAuthor]
    def delete_ticket(self, requets, pk):
        response = Response()
        ticket = Ticket.objects.filter(pk=pk) 
        ticket.delete()
        return response
    



