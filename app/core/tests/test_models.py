"""
Tests for models.
"""
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

class UserModels(TestCase):
    """Test models."""

    def test_create_device(self):
        """test creating device is successful."""
        dt = datetime.now()
        device = models.Device.objects.create(
            device_id='SomeDeviceId',
            device_info = {'info': 'some info', 'some number': 123},
            created_at = dt
        )
        self.assertEqual(device.created_at, dt)
        self.assertEqual(str(device), f'{device.device_id}: {device.device_info}')
        self.assertGreaterEqual(device.updated_at, device.created_at)
