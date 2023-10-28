from rest_framework import serializers
from .models import Ticket
from users.serializers import UserSerializer
import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError
from users.models import User



class TicketsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    kind = serializers.ChoiceField(choices=Ticket.STATUS, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = ['subject', 'body', 'kind', 'created', 'author', 'id', 'comments']
        extra_kwargs = {
            'id': {'read_only': True},
            'kind': {'read_only': True},
            'author': {'read_only': True},
            'created': {'read_only': True},
            'comments': {'read_only': True}
        }


class TicketsSerializerUpdateKind(serializers.ModelSerializer):
    kind = serializers.ChoiceField(choices=Ticket.STATUS)
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Ticket
        fields = ['subject', 'body', 'kind', 'created', 'author', 'id']
        extra_kwargs = {
            'id': {'read_only': True},
            'author': {'read_only': True},
            'created': {'read_only': True},
            'subject': {'read_only': True},
            'body': {'read_only': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance


