from rest_framework import serializers
from .models import Order, Notification, Order_a_call
from user.models import Profile
from rest_framework.exceptions import ValidationError



class OrderSerializer(serializers.ModelSerializer):
    from_creator_administrator = serializers.ReadOnlyField(source='from_creator_administrator.username')

    class Meta:
        model = Order
        fields = ['id', 'from_creator_administrator', 'to_recipient_user', 'to_recipient_animators', 
                 'notes', 'activity', 'created_at', 'changes', 'data_time_order', 'personage', 
                 'sale', 'price', 'kombo', 'program']
        extra_kwargs = {
            'id': {'read_only': True},
            'from_creator_administrator': {'read_only': True},
            'activity': {'read_only': True},
            'created_at' : {'read_only': True},
            'changes' : {'read_only': True},
        }


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']



class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "recipient", "created_at", "read", "message")
        extra_kwargs = {
            "recipient": {"read_only": True},
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "read": {"read_only": True},
        }


class Order_a_callSerializer(NotificationSerializer):
    from_creator_user = serializers.ReadOnlyField(source='from_creator_user.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')
    phone_number = serializers.ReadOnlyField()
    class Meta:
        model = Order_a_call
        fields = ("id", "from_creator_user","time_to_call", 
                  "info_for_users", "recipient", "phone_number", "message")
        extra_kwargs = {
            "from_creator_user": {"read_only": True},
            "info_for_users": {"read_only": True},
            "recipient": {"read_only": True},
            "phone_number": {"read_only": True},
        }


class NotificationSerializeRead(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("read", )
