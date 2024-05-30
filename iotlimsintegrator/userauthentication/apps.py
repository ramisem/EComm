from django.apps import AppConfig


class UserauthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "iotlimsintegrator.views.MyAdminSite"
    name = 'userauthentication'
    verbose_name = 'Users'
