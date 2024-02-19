from django.core.files.uploadedfile import SimpleUploadedFile
from core.models import Order


def create_order(**params) -> Order:
    """Helper function. Create device."""

    file_content = b'This is a test file content.'
    file = SimpleUploadedFile('test_file.txt', file_content)

    defaults = {
        "order_text": 'some order text',
        "order_file": file
    }
    defaults.update(params)

    order = Order.objects.create(**defaults)
    return order
