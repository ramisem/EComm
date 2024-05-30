from django.apps import AppConfig


class MasterdataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "iotlimsintegrator.views.MyAdminSite"
    name = 'masterdata'
    verbose_name = 'Monitoring Data'
