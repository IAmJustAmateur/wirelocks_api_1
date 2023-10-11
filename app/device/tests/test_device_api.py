"""
Test for device models
"""
import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Device,
    DeviceMessage
)

def create_user():
    """Helper function: create user"""
    user = get_user_model().objects.create_user(
        'test@example.com',
        'testpass123',
    )
    return user

def create_device(**params):
    """Helper function: create device"""
    device_info = {'info': 'some info', 'some number': 123}
    defaults = {
        'device_id': 'ThisIsDeviceId',
        'device_info': json.dumps(device_info)
    }
    defaults.update(params)
    device = Device.objects.create(**defaults)
    return device

class DeviceModelTests(TestCase):
    """Tests for device"""

    def test_create_device_success(self):
        device = create_device()
        self.assertEqual(device.device_id, )