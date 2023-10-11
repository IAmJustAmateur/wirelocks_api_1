"""
Database models
"""

from datetime import datetime
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Device(models.Model):
    """Device model"""
    device_id = models.CharField(max_length=255, unique=True, blank=False)
    device_info = models.JSONField(default=None, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.device_id}: {self.device_info}'

    def save(self, *args, **kwargs) -> None:
        d = datetime.now()
        self.updated_at = d
        return super().save(*args, **kwargs)


class DeviceMessage(models.Model):
    """Device message"""
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    message_text = models.TextField(null=False, blank=False)
    other_info = models.JSONField(default=None, blank=True, null=True)
    received_at = models.DateTimeField()
    updated_at = models.DateTimeField()
