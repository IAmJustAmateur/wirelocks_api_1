"""
Views for  the device APIs.
"""

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework import viewsets

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Device,
    DeviceMessage
)
from . import serializers


class DeviceViewSet(viewsets.ModelViewSet):
    """View for manage topic APIs."""
    serializer_class = serializers.DeviceDetailSerializer
    queryset = Device.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve devices."""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DeviceSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new device."""
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'device_id',
                OpenApiTypes.INT,
                description='Filter by devices.',
            ),
            OpenApiParameter(
                'device',
                OpenApiTypes.STR,
                description='Filter by device name.',
            ),
        ]
    )
)
class DeviceMessageViewSet(viewsets.ModelViewSet):
    """View for manage topic APIs."""
    serializer_class = serializers.DeviceMessageDetailSerializer
    queryset = DeviceMessage.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DeviceMessageSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new message."""
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

    def get_queryset(self):
        """Filter queryset to device."""

        b_device_id = bool(
            int(self.request.query_params.get('device_id', 0))
        )
        b_device = bool(
            self.request.query_params.get('device', 0)
        )

        queryset = self.queryset
        if b_device_id:
            device_id = self.request.query_params.get('device_id', 0)
            queryset = queryset.filter(
                device=device_id
            )

        if b_device:
            device_name = self.request.query_params.get('device', 0)
            device_id = Device.objects.filter(device_id=device_name)
            queryset = queryset.filter(
                device__id__in=device_id
            )

        return queryset.order_by('-id').distinct()
