"""
URL mapping for the device app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter


from device import views


router = DefaultRouter()
router.register('devices', views.DeviceViewSet)
router.register('devicemessages', views.DeviceMessageViewSet)

app_name = 'device'

urlpatterns = [
    path('', include(router.urls)),
]
