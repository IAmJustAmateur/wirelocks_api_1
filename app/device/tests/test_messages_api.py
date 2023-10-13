"""
Test for device APIs.
"""
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import DeviceMessage

from device.serializers import (
    DeviceMessageSerializer,
    DeviceMessageDetailSerializer,
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
        serializer = DeviceMessageSerializer(deviceMessages, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_deviceMessage_detail(self):
        """Test retrieving device message detail."""

        device = create_device()
        msg = create_device_message(device)
        url = detail_url(msg.id)

        res = self.client.get(url)
        serializer = DeviceMessageDetailSerializer(msg)
        self.assertEqual(res.data, serializer.data)

    def test_filtering_messages_by_device(self):
        """Test filtering messages by device"""

        device1 = create_device()
        device2 = create_device(device_id="Some other device id")

        msg1 = create_device_message(device=device1)
        msg2 = create_device_message(device=device2)
        msg3 = create_device_message(device=device1)

        res = self.client.get(DEVICEMESSAGES_URL, {'device_id': device1.id})
        deviceMessages = DeviceMessage.objects.all() \
            .order_by('-id').filter(device=device1)
        serializer = DeviceMessageSerializer(deviceMessages, many=True)
        self.assertEqual(res.data, serializer.data)

        self.assertIn(msg1, deviceMessages)
        self.assertIn(msg3, deviceMessages)
        self.assertNotIn(msg2, deviceMessages)
