from rest_framework import serializers
from .models import Personage
from user.models import Profile
from rest_framework.exceptions import ValidationError

class PersonageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    class Meta:
        model = Personage
        fields = ['id', 'creator', 'name', 'description', 'image', 'activity', 'life_size_puppet', ]
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True},
            'activity': {'read_only': True},
            'life_size_puppet' : {'read_only': True},

        }


class PersonageUpdateSerializerForAdministrator(serializers.ModelSerializer):

    class Meta:
        model = Personage
        fields = ['id', 'creator', 'name', 'description', 'image', 'activity', 'life_size_puppet']
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True},
        }

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value) 
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['my_likes']
        extra_kwargs = {
            'my_likes': {'read_only': True},
        }