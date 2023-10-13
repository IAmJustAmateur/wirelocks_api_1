"""
Test for device APIs.
"""
import json
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Device,
    DeviceMessage
)

from device.serializers import (
    DeviceSerializer,
    DeviceDetailSerializer,
    DeviceMessageSerializer,
)

from . utils import create_user, create_device, create_device_message

DEVICEMESSAGES_URL = reverse('device:devicemessage-list')


def detail_url(device_id):
    """create and return deviceMessage url"""
    return reverse('device:devicemessage-detail', args=[device_id])


class PublicDeviceMessageAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(DEVICEMESSAGES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDeviceMessageApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_deviceMessages(self):
        """Test retrieving a list of device messages."""

        device1 = create_device()
        device2 = create_device(device_id="Some other device id")

        create_device_message(device=device1)
        create_device_message(device=device2)

        res = self.client.get(DEVICEMESSAGES_URL)

        deviceMessages = DeviceMessage.objects.all().order_by('-id')
        serializer = DeviceSerializer(deviceMessages, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data[0], serializer.data[0])
