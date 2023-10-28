from rest_framework import serializers
from .models import User



class UserSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'intro', 'city', 'slug', 'tickets', 'comments']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'slug': {'read_only': True},
            'tickets': {'read_only': True},
            'comments': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    

class UserUpdateSerializer(serializers.ModelSerializer):
    tickets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'intro', 'city', 'slug', 'tickets']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'slug': {'read_only': True},
            'email': {'read_only': True},
            'tickets': {'read_only': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance

