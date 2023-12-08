from rest_framework import serializers
from .models import Program
from rest_framework.exceptions import ValidationError



class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ['name','price', 'time', 'description',]
        extra_kwargs = {
            'name': {'read_only': True},
            'price': {'read_only': True},
            'time': {'read_only': True},
            'description': {'read_only': True},
        }