# Generated by Django 3.1.2 on 2020-11-26 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_app', '0002_auto_20201123_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='exam_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]