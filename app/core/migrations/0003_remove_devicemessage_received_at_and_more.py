# Generated by Django 4.2.1 on 2023-10-12 06:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_device_devicemessage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devicemessage',
            name='received_at',
        ),
        migrations.AddField(
            model_name='devicemessage',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 10, 12, 6, 34, 37, 961942)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='devicemessage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
