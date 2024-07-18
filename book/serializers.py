from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Book
        fields = ["id", "owner", "author", "title", "year", "status"]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "status": {"read_only": True}
        }


class UpdateBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["status"]
     