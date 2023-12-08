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
            str(device),
            (
                f'{device.device_id}: {device.device_info}: '
                f'{device.created_at}: {device.updated_at}'
            )
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
            (
                f'{device.device_id}: {deviceMessage.id}: This is message: '
                f'{deviceMessage.created_at}: {deviceMessage.updated_at}'
            )

        )
        self.assertGreaterEqual(deviceMessage.created_at, device.created_at)

    def test_create_deviceProgram(self):
        """Test creating device program is successful."""

        user = models.User.objects.create(
            email = 'email@example.com',
            password = "testpass",
            is_superuser = True,
            is_developer = True,
            is_staff = True,
            is_active = True
        )

        device = models.Device.objects.create(
            device_id='SomeDeviceId',
            device_info={'info': 'some info', 'some number': 123},
        )

        program = models.DeviceProgram.objects.create(
            # device = device,
            program_id = "this is simple test program",
            program_code = "this is program code",
            developer = user
        )
        self.assertEqual(str(program), "this is program code")
        self.assertEqual(program.program_id, "this is simple test program")
        self.assertEqual(program.developer.id, user.id)
