# Generated by Django 3.1.2 on 2020-11-30 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0006_auto_20201130_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalcompensation',
            name='linked',
            field=models.BooleanField(default=False),
        ),
    ]
