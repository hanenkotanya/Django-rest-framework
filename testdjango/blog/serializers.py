from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source="creator.username")

    class Meta:
        model = Post
        fields = ["id", "creator", "name", "activity", "created_at", "changes", "text"]
        extra_kwargs = {
            "id": {"read_only": True},
            "creator": {"read_only": True},
            "activity": {"read_only": True},
            "created_at": {"read_only": True},
            "changes": {"read_only": True},
        }


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "name", "text", "changes", "activity"]
        extra_kwargs = {
            "id": {"read_only": True},
            "changes": {"read_only": True},
        }
