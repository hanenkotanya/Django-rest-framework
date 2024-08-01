from rest_framework import serializers
from .models import Player
from rest_framework.exceptions import ValidationError

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model = Player
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
            raise serializers.ValidationError('Не правильные данные')     

        
class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ['player_id', 'email', 'password', 'username', 'points','first_entrance', 'created']
        extra_kwargs = {
            'password': {'write_only': True},
            'player_id': {'read_only': True},
            'points': {'read_only': True},
            'created': {'read_only': True},
            'first_entrance': {'read_only': True},
            
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        email = validated_data.get('email')
        username = validated_data.get('username')
        try:
            player = Player.objects.create_user(email=email, password=password, username=username)
        except ValidationError as e:
            raise serializers.ValidationError({'email': e})
        return player