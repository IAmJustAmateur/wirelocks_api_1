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

from core.models import Order
from . import serializers


class OrderViewSet(viewsets.ModelViewSet):
    """View for manage Order APIs."""
    serializer_class = serializers.OrderDetailSerializer
    queryset = Order.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve devices."""
        return self.queryset.order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.OrderSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new device."""
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)

