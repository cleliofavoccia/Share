# Generated by Django 3.2.3 on 2021-07-14 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0007_auto_20210711_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
