"""
URL mapping for the program app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

import deviceprogram.views as _v
print(dir(_v))

from deviceprogram.views import DeviceProgramViewSet

app_name = 'deviceprogram'

router = DefaultRouter()
router.register('deviceprogram', DeviceProgramViewSet)
#print (router.get_default_basename())
#print (router.get_default_basename(DeviceProgramViewSet))

urlpatterns = [
    path('', include(router.urls)),
]
