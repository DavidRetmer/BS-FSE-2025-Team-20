from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'community'
    verbose_name = 'Football Community'

    def ready(self):
        """Import signal handlers when the app is ready"""
        import community.signals  # noqa
