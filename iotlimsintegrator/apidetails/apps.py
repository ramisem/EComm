from django.apps import AppConfig


class ApidetailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "iotlimsintegrator.views.MyAdminSite"
    name = 'apidetails'
    verbose_name = 'APIs'
