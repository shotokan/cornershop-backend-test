# Generated by Django 3.0.8 on 2021-06-30 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20210630_1404'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='option_selected',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.MenuOptions'),
        ),
    ]