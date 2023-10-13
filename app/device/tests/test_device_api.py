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
)

from device.serializers import (
    DeviceSerializer,
    DeviceDetailSerializer,
)

from . utils import create_user, create_device

DEVICES_URL = reverse('device:device-list')


def detail_url(device_id):
    """create and return device url"""
    return reverse('device:device-detail', args=[device_id])


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

    def test_create_device(self):
        """Test creating device"""
        device_info = {'info': 'some info', 'some number': 123}
        payload = {
            "device_id": 'SomeDeviceId',
            "device_info": json.dumps(device_info),
        }
        res = self.client.post(DEVICES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        device = Device.objects.get(id=res.data['id'])

        self.assertEqual(device.device_id, payload["device_id"])
        self.assertEqual(device.device_info, device_info)

    def test_partial_update(self):
        """Test partial update of a device."""
        device = create_device()
        device_info = {
            "info": "some other info",
            "some text": "simple text"
        }
        payload = {
            "device_info":  json.dumps(device_info)
        }
        url = detail_url(device_id=device.id)
        res = self.client.patch(url, payload)

        device.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(device.device_info, device_info)
