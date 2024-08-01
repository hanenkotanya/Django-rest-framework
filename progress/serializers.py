from rest_framework import serializers
from .models import LevelPrize, PlayerLevel
from rest_framework.exceptions import ValidationError



class PlayerLevelSerializer(serializers.ModelSerializer):
    player = serializers.ReadOnlyField(source='player.username')
    is_complited = True
    class Meta:
        model = PlayerLevel
        fields = ['player', 'level', 'completed', 'is_completed', 'score']
        extra_kwargs = {
            'player': {'read_only': True},
            'completed': {'read_only': True},    
            'is_completed': {'read_only': True},  
            'score': {'read_only': True},     
        }


class PlayerPrizeSerializer(serializers.ModelSerializer):
    player = serializers.ReadOnlyField(source='player')
    class Meta:
        model = LevelPrize
        fields = ['player', 'prize', 'received']
        extra_kwargs = {
            'player': {'read_only': True},
            'received': {'read_only': True},       
        }
