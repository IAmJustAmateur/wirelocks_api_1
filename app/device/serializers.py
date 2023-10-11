"""
Serializers for device APIs
"""
from rest_framework import serializers

from core.models import (
    Device,
    DeviceMessage,
)

class DeviceSerializer(serializers.ModelSerializer):
    """Serializers for devices."""

    class  Meta:
        model = Device
        fields = ['id', 'device_id', 'device_info']
        read_only_fields = ['id' ]


class DeviceMessageSerializer(serializers.ModelSerializer):
    """Serializer for device message."""

    class Meta:
        model = DeviceMessage
        fields = ['id', 'message_text', 'other_info']
        read_only_fields = ['id']
