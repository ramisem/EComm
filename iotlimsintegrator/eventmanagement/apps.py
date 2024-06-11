from django.apps import AppConfig


class EventmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "iotlimsintegrator.views.MyAdminSite"
    name = 'eventmanagement'
    verbose_name = "Rule Engine"
