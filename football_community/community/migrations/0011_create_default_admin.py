from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_admin(apps, schema_editor):
    User = apps.get_model('community', 'User')
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create(
            username='admin',
            email='admin@example.com',
            password=make_password('admin123'),  # Default password: admin123
            is_staff=True,
            is_superuser=True,
            is_moderator=True,
            can_moderate_content=True,
            can_manage_events=True,
            can_ban_users=True
        )

def reverse_default_admin(apps, schema_editor):
    User = apps.get_model('community', 'User')
    User.objects.filter(username='admin').delete()

class Migration(migrations.Migration):
    dependencies = [
        ('community', '0010_alter_event_location_latitude_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_admin, reverse_default_admin),
    ] 