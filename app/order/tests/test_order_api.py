"""
Test for order APIs.
"""
from django.test import TestCase
from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Order,
)

from order.serializers import (
    OrderSerializer,
    OrderDetailSerializer,
)

from . utils import create_order
from device.tests.utils import create_user

ORDERS_URL = reverse('order:order-list')

def detail_url(order_id):
    """create and return device url"""
    return reverse('order:order-detail', args=[order_id])


class PublicOrderAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ORDERS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrdersApiTests(TestCase):
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

        create_order()
        create_order(order_text="some new order")

        res = self.client.get(ORDERS_URL)

        devices = Order.objects.all().order_by('-id')
        serializer =  OrderSerializer(devices, many=True)
        self.assertEqual (res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_order_detail(self):
        """Test get device detail."""
        order = create_order()
        url = detail_url(order_id=order.id)
        res = self.client.get(url)
        serializer = OrderDetailSerializer(order)
        self.assertEqual(res.data['id'], serializer.data['id'])
        self.assertEqual(res.data['order_text'], serializer.data['order_text'])
        self.assertEqual(res.data['order_file'], f"http://testserver{serializer.data['order_file']}")

    def test_create_order(self):
        """Test creating device"""
        file_content = b'This is a test file content.'
        order_file = SimpleUploadedFile('test_file.txt', file_content)
        payload = {
            "order_text": 'some order',
            "order_file": order_file,
        }
        res = self.client.post(ORDERS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data['id'])

        self.assertEqual(order.order_text, payload["order_text"])
