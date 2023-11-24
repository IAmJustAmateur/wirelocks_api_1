# Generated by Django 4.2.1 on 2023-11-24 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_devicemessage_received_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.device')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
