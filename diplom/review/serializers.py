from rest_framework import serializers
from .models import Review



class ReviewSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.username')

    class Meta:
        model = Review
        fields = ['id', 'from_user', 'personage', 'kombo', 
                 'description', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'from_user': {'read_only': True},
            'created_at' : {'read_only': True},
        }