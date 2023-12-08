"""
Serializers for program APIs
"""
from rest_framework import serializers

from core.models import (
    Device,
    DeviceProgram
)

class DeviceProgramSerializer(serializers.ModelSerializer):
    """Serializer for device program."""

    class Meta:
        model = DeviceProgram
        fields = ['id', 'device', 'developer']
        read_only_fields = ['id']


class DeviceProgramDetailSerializer(serializers.ModelSerializer):
    """Serializer for device program detail. """

    class Meta:
        model = DeviceProgram
        fields = DeviceProgramSerializer.Meta.fields + ["program_id", "program_code", "executionState", "errorCode"]
        read_only_fields = ['id']
