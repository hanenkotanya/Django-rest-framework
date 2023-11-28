from rest_framework import serializers
from .models import Personage, Kombo
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

class PersonageOneListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personage
        fields = ['name', 'description', 'image']
        extra_kwargs = {
            'name': {'read_only': True},
            'description': {'read_only': True},
            'image': {'read_only': True},
        }


class PersonageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personage
        fields = ['name', 'image', 'id']
        extra_kwargs = {
            'name': {'read_only': True},
            'image': {'read_only': True},
        }
 


class KomboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kombo
        fields = ['personage1', 'personage2', 'name', 'description', 'image']



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


class PersonageSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personage
        fields = ['name', 'description', 'image', 'activity', 'life_size_puppet',]