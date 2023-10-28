from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from users.models import User
from tickets.models import Ticket



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    kind = serializers.ChoiceField(choices=Comment.STATUS, read_only=True)
   # ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.alias().filter(author = author) or author.role == "Админ")
    class Meta:
        model = Comment
        fields = ['ticket', 'body', 'kind', 'created', 'author', 'id']
        extra_kwargs = {
            'id': {'read_only': True},
            'kind': {'read_only': True},
            'author': {'read_only': True},
            'created': {'read_only': True}
        }

class CommentSerializerUpdateKind(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=Comment.STATUS)
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Comment
        fields = ['ticket', 'body', 'kind', 'created', 'author', 'id']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True},
            'created': {'read_only': True},
            'ticket': {'read_only': True},
            'body': {'read_only': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance


