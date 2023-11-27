"""
Database models
"""

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

    is_developer = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Device(TimeStampMixin):
    """Device model"""
    device_id = models.CharField(max_length=255, unique=True, blank=False)
    device_info = models.JSONField(default=None, blank=True, null=True)

    def __str__(self):
        return (
            f'{self.device_id}: {self.device_info}: '
            f'{self.created_at}: {self.updated_at}'
        )


class DeviceMessage(TimeStampMixin):
    """Device message"""
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    message_text = models.TextField(null=False, blank=False)
    other_info = models.JSONField(default=None, blank=True, null=True)

    def __str__(self):
        return (
            f'{self.device.device_id}: {self.id}: {self.message_text}: '
            f'{self.created_at}: {self.updated_at}'
        )

class DeviceProgram(TimeStampMixin):
    """Device program"""
    device = models.ForeignKey(Device, null=False, on_delete=models.CASCADE)
    program_id = models.CharField(null=False, blank=False, max_length=255)
    developer = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    code = models.TextField(null=False, blank=False)
    executionState_choices = [
        ('awaiting_execution', 'Awaiting Execution'),
        ('execution_started', 'Execution Started'),
        ('execution_finished_ok', 'Execution Finished with OK'),
        ('execution_failed_error_code', 'Execution Failed with Error Code')
    ]
    executionState = models.CharField(
        max_length=30,
        choices=executionState_choices,
        default='awaiting_execution'
    )
    errorCode = models.CharField(max_length=30, blank=True)
