# Generated by Django 3.0.8 on 2021-07-01 06:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20210630_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todaymenu',
            name='option1',
        ),
        migrations.RemoveField(
            model_name='todaymenu',
            name='option2',
        ),
        migrations.RemoveField(
            model_name='todaymenu',
            name='title',
        ),
    ]
