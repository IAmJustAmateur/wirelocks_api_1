"""
Utils for tests.
"""
import json
from django.contrib.auth import get_user_model

from core.models import (
    Device,
    DeviceMessage
)


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_device(**params) -> Device:
    """Helper function. Create device."""
    defaults = {
        "device_id": 'SomeDeviceId',
        "device_info": json.dumps({'info': 'some info', 'some number': 123}),
    }
    defaults.update(params)

    device = Device.objects.create(**defaults)
    return device


def create_device_message(device, **params):
    """Helper function. Create device message."""
    defaults = {
        'message_text': 'some device message',
        "other_info": json.dumps({'info': 'some info', 'some number': 123}),
    }
    defaults.update(params)
    deviceMessage = DeviceMessage.objects.create(device=device, **defaults)
    return deviceMessage
