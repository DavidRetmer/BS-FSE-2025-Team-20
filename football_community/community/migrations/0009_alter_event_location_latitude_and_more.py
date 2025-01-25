# Generated by Django 4.2.18 on 2025-01-24 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0008_alter_event_location_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location_latitude',
            field=models.DecimalField(blank=True, decimal_places=50, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_longitude',
            field=models.DecimalField(blank=True, decimal_places=50, max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_latitude',
            field=models.DecimalField(blank=True, decimal_places=50, help_text="User's latitude coordinate", max_digits=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_longitude',
            field=models.DecimalField(blank=True, decimal_places=50, help_text="User's longitude coordinate", max_digits=50, null=True),
        ),
    ]
