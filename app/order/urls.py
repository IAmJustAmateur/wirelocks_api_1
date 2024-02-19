"""
URL mapping for the Order app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter


from order import views

router = DefaultRouter()
router.register('orders', views.OrderViewSet)

app_name = 'order'

urlpatterns = [
    path('', include(router.urls)),
]
