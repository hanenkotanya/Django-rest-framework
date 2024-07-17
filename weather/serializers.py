from rest_framework import serializers
from .models import Search_History


class CitySerializer(serializers.Serializer):
    class Meta:
        model = Search_History
        fields = ("user", "name_city", "date")
        extra_kwargs = {
            "date": {"read_only": True},
        }
