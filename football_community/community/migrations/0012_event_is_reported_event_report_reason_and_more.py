# Generated by Django 4.2.18 on 2025-01-24 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0011_create_default_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='report_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='reported_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='is_reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='report_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='reported_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_reported',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='report_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='reported_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
