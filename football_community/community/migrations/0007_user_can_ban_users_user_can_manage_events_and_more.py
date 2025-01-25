# Generated by Django 4.2.18 on 2025-01-23 16:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_alter_user_options_user_is_moderator'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_ban_users',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='can_manage_events',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='can_moderate_content',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='location_updated_at',
            field=models.DateTimeField(blank=True, help_text='When the location was last updated', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='max_players',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(2), django.core.validators.MaxValueValidator(22)]),
        ),
        migrations.AlterField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participated_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='skill_level_filter',
            field=models.CharField(blank=True, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('professional', 'Professional')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='availability_days',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='availability_time_slots',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('morning', 'Morning (6 AM - 12 PM)'), ('afternoon', 'Afternoon (12 PM - 5 PM)'), ('evening', 'Evening (5 PM - 10 PM)')], max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_latitude',
            field=models.DecimalField(blank=True, decimal_places=6, help_text="User's latitude coordinate", max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='location_longitude',
            field=models.DecimalField(blank=True, decimal_places=6, help_text="User's longitude coordinate", max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='skill_level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('professional', 'Professional')], default='beginner', max_length=20),
        ),
    ]
