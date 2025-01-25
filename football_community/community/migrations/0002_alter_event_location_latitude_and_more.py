# Generated by Django 4.2.18 on 2025-01-23 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location_latitude',
            field=models.DecimalField(decimal_places=6, max_digits=30),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_longitude',
            field=models.DecimalField(decimal_places=6, max_digits=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_latitude',
            field=models.DecimalField(decimal_places=6, max_digits=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_longitude',
            field=models.DecimalField(decimal_places=6, max_digits=30, null=True),
        ),
    ]
