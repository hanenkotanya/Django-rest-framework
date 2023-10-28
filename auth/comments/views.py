from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer, CommentSerializerUpdateKind
from rest_framework import generics
from .permissions import IsAdminOrAuthor, IsOnlyAdmin, NotAythor
import jwt
from rest_framework.exceptions import AuthenticationFailed
from tickets.models import Ticket

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


class CommentCreateList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrAuthor]
    def perform_create(self, serializer):
        serializer.save(author = get_user(self.request))

class CommentOne(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerUpdateKind
    permission_classes = [IsAdminOrAuthor]
    def get_one_comment(self, requets, pk):
        comment = Comment.objects.filter(pk=pk) 
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)


class CommentOneUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerUpdateKind
    permission_classes = [NotAythor]
    def update_kind(self, request, pk):
        comment = Comment.objects.filter(pk=pk) 
        self.check_object_permissions(self.request, comment)
        serializer_data = request.data.get(comment)
        serializer = self.serializer_class(data=serializer_data, partial=True)
        serializer.is_valid(raise_exception =True)
        serializer.save()
        return Response (serializer.data)

    

