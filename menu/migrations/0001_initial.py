# Generated by Django 3.0.8 on 2021-06-25 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TodayMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('option1', models.TextField()),
                ('option2', models.TextField()),
                ('created', models.DateField(auto_now_add=True)),
                ('modified', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
