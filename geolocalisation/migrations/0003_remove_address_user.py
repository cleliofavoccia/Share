# Generated by Django 3.2.3 on 2021-06-09 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geolocalisation', '0002_address_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
    ]
