# Generated by Django 3.2.3 on 2021-07-10 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geolocalisation', '0003_remove_address_user'),
        ('group', '0005_group_members_points'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_of_group', to='geolocalisation.address'),
        ),
    ]
