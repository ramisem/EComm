from django.apps import AppConfig


class TaskConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "iotlimsintegrator.views.MyAdminSite"
    name = 'task'
    verbose_name = 'Tasks'
