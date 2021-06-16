# Generated by Django 3.2.3 on 2021-06-08 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delete_group_vote', models.BooleanField(default=False)),
                ('modify_group_vote', models.BooleanField(default=False)),
                ('delete_member_vote', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Estimation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.IntegerField()),
            ],
        ),
    ]
