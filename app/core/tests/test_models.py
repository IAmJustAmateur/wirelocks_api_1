"""
Tests for models.
"""
from django.test import TestCase
from core import models


class TestModels(TestCase):
    """Test models."""

    def test_create_device(self):
        """test creating device is successful."""
        device = models.Device.objects.create(
            device_id='SomeDeviceId',
            device_info={'info': 'some info', 'some number': 123},
        )
        self.assertEqual(
            str(device), f'{device.device_id}: {device.device_info}'
        )
        self.assertGreaterEqual(device.updated_at, device.created_at)

    def test_create_deviceMessage(self):
        """Test creating device message is successful."""
        device = models.Device.objects.create(
            device_id='SomeDeviceId',
            device_info={'info': 'some info', 'some number': 123},
        )
        deviceMessage = models.DeviceMessage.objects.create(
            device=device,
            message_text="This is message",
            other_info={'info': 'some info', 'some array': [1, 2, 3]}
        )
        self.assertEqual(
            str(deviceMessage),
            f'{device.device_id}: {deviceMessage.id}: This is message'
        )
        self.assertGreaterEqual(deviceMessage.created_at, device.created_at)
