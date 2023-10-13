"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']
    search_fields = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


class DeviceAdmin(admin.ModelAdmin):
    ordering = ['id']
    fields = [
        'device_id',
        'device_info',
        'created_at',
        'updated_at',
    ]
    readonly_fields = ['created_at', 'updated_at']


class DeviceMessageAdmin(admin.ModelAdmin):
    ordering = ['id']
    fields = [
        'device',
        'message_text',
        'other_info',
        'created_at',
        'updated_at',
    ]
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(models.User, UserAdmin)

admin.site.register(models.Device, DeviceAdmin)
admin.site.register(models.DeviceMessage, DeviceMessageAdmin)
