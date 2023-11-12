from rest_framework import serializers
from .models import Personage
from rest_framework.exceptions import ValidationError

class PersonageSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.email')
    class Meta:
        model = Personage
        fields = ['id', 'creator', 'name', 'description', 'image', 'activity', 'life_size_puppet', 'animators_1_4_years', 'animators_5_9_years', 'animators_9_14_years']
        extra_kwargs = {
            'id': {'read_only': True},
            'creator': {'read_only': True},
            'activity': {'read_only': True},
            'life_size_puppet' : {'read_only': True},
            'animators_1_4_years' : {'read_only': True}
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