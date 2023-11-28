from rest_framework import serializers
from .models import User, Profile
from rest_framework.exceptions import ValidationError

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            return data
        else:
            raise serializers.ValidationError('не правильные данные')     

        
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'slug', 'username']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'slug': {'read_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.get('email')
        username = validated_data.get('username')
        try:
            user = User.objects.create_user(email=email, password=password, username=username)
        except ValidationError as e:
            raise serializers.ValidationError({'email': e})
        return user

    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image', 'role', 'intro', 'full_name', 'my_likes', 'phone_number']


class ProfileLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['my_likes']


class ProfileUpdateSerializerForUser(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user','image','full_name', 'phone_number']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},
    
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance
    

class ProfileUpdateSerializerForAnimators(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user','image', 'full_name', 'intro']
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'read_only': True},

        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance
    

class AnimotorForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'intro', 'full_name']
    