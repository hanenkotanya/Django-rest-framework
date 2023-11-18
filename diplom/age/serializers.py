from rest_framework import serializers
from .models import Age
from rest_framework.exceptions import ValidationError

class AgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Age
        fields = ['animators_for_years' ]
        extra_kwargs = {
            'animators_for_years': {'read_only': True},
        }