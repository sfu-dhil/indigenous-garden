from django.apps import AppConfig


class IndigenousGardenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'indigenous_garden_app'
    verbose_name = 'Indigenous Garden'

    def ready(self):
        import indigenous_garden_app.signals