"""
Test for device APIs.
"""
import json
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

# from core.models import (
#     Device,
#     DeviceProgram,
#     User
# )

# from programs.serializers import (
#     DeviceProgramSerializer,
# )

from device.tests.utils import create_user, create_device, create_program

PROGRAMS_URL = reverse('deviceprogram:deviceprograms-list')

def detail_url(program_id):
    """create and return program url"""
    return reverse('deviceprograms:deviceprogram-detail', args=[program_id])


class PublicProgramAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PROGRAMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
