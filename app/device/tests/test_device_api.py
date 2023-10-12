"""
Test for device APIs.
"""
import json
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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

DEVICES_URL = reverse('device:device-list')


def detail_url(device_id):
    """create and return device url"""
    return reverse('device:device-detail', args=[device_id])


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_device(**params):
    """Helper function. Create device."""
    defaults = {
            "device_id": 'SomeDeviceId',
            "device_info": json.dumps({'info': 'some info', 'some number': 123}),
    }
    defaults.update(params)

    device = Device.objects.create(**defaults)
    return device


def create_device_message(**params):
    """Helper function. Create device message."""
    pass

class PublicDeviceAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(DEVICES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDeviceApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_devices(self):
        """Test retrieving a list of devices."""

        create_device()
        create_device(device_id="Some other device id")

        res = self.client.get(DEVICES_URL)

        devices = Device.objects.all().order_by('-id')
        serializer = DeviceSerializer(devices, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_device_detail(self):
        """Test get device detail."""
        device = create_device()
        url = detail_url(device_id=device.id)
        res = self.client.get(url)
        serializer = DeviceDetailSerializer(device)
        self.assertEqual(res.data, serializer.data)
