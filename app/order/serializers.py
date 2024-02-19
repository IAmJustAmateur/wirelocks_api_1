"""
Serializers for order APIs
"""
from rest_framework import serializers

from core.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for order."""

    class Meta:
        model = Order
        fields = ['id', 'order_text']
        read_only_fields = ['id']


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for order detail."""
    class Meta:
        model = Order
        fields = OrderSerializer.Meta.fields + ["order_file"]
        read_only_fields = ['id']