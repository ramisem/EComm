from admin_tools_stats.admin import DashboardStatsAdmin
from django.contrib import messages
from django.utils.html import format_html

from dashboard.forms import CustomDashboardStatsForm
from dashboard.models import CustomDashboardStats
from iotlimsintegrator.views import my_admin_site


class CustomDashboardStatsAdmin(DashboardStatsAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('graph_key', 'graph_title'),
            'classes': ('wide',),
        }),
        ('App/Models', {
            'fields': ('model_app_name', 'model_name', 'date_field_name', 'operation_field_name', 'distinct'),
            'classes': ('wide',),
        }),
        ('Operation', {
            'fields': ('allowed_type_operation_field_name', 'type_operation_field_name'),
            'classes': ('wide',),
        }),
        ('Chart Types', {
            'fields': ('allowed_chart_types', 'default_chart_type'),
            'classes': ('wide',),
        }),
        ('Time Scale', {
            'fields': ('allowed_time_scales', 'default_time_scale', 'default_time_period'),
            'classes': ('wide',),
        }),
    )
    list_display = (
        "graph_key",
        "analytics_link",
        "graph_title",
        "model_name",
        "created_date",
        "default_chart_type",
    )
    date_hierarchy = 'created_date'
    list_filter = [
        "graph_key",
        "model_name",
        "default_chart_type",
    ]

    inlines = []

    form = CustomDashboardStatsForm

    def save_model(self, request, obj, form, change):
        try:
            if request.user.is_authenticated:
                obj.show_to_users = True
                obj.is_visible = True
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error saving model: {e}")
            return

    def analytics_link(self, obj):
        return format_html(
            "<a href='{url}?show={key}' target='_blank'>Click To Open</a>",
            url='/dashboard/customanalytics/',
            key=obj.graph_key,
        )

    class Media:
        js = ('js/dashboard/maint_dashboard.js', 'js/util/util.js',)


my_admin_site.register(CustomDashboardStats, CustomDashboardStatsAdmin)
