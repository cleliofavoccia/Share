# Generated by Django 3.2.5 on 2021-07-27 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group_member', '0004_alter_groupmember_points_posseded'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupmember',
            name='points_penalty',
            field=models.IntegerField(default=0),
        ),
    ]