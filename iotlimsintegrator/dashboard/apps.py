from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    default_site = "iotlimsintegrator.views.MyAdminSite"
    name = 'dashboard'
    verbose_name = 'Dashboard'
