from django.apps import AppConfig


class UsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'us'


    def ready(self):
        import us.signals