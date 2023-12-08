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
    DeviceProgram
)
from . import serializers

class DeviceProgramViewSet(viewsets.ModelViewSet):
    """View for manage topic APIs."""
    serializer_class = serializers.DeviceProgramDetailSerializer
    queryset = DeviceProgram.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.DeviceProgramSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new message."""
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

    def get_queryset(self):
        """Filter queryset to user."""
        user = self.request.user
        if user.is_authenticated:
            if user.is_superuser:
                return DeviceProgram.objects.all()
            else:
                return DeviceProgram.objects.filter(user=user)
        return DeviceProgram.objects.none()
