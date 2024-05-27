import json

from django.conf import settings
from django.contrib import admin, messages
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_celery_beat.admin import PeriodicTaskAdmin, PeriodicTaskForm

from task.models import CustomPeriodicTask, TaskAudit
from userauthentication.models import User


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, models.Model):
            return obj.pk  # Return the primary key for models
        return super().default(obj)


class CustomPeriodicTaskForm(PeriodicTaskForm):
    def clean(self):
        return self.cleaned_data


class CustomPeriodicAdmin(PeriodicTaskAdmin):
    list_display = ('name', 'description', 'enabled', 'event_rule_id', 'interval', 'start_time',
                    'last_run_at', 'created_by')
    list_filter = ['enabled', 'event_rule_id', 'name', 'start_time', 'last_run_at', 'created_by']
    search_fields = ()
    actions = ('enable_tasks', 'disable_tasks')

    form = CustomPeriodicTaskForm

    fieldsets = (
        (None, {
            'fields': ('name', 'event_rule_id', 'enabled', 'created_by', 'description',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('interval', 'start_time', 'last_run_at'),
            'classes': ('extrapretty', 'wide'),
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            obj.task = getattr(settings, 'APPLICATION_TASK_HANDLER')
            obj.args = json.dumps([obj.event_rule_id, obj.name], cls=CustomJSONEncoder)
            if request.user.is_authenticated:
                username = request.user.username
                user_map_obj = User.objects.get(username=username)
                obj.created_by = user_map_obj
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error saving model: {e}")
            return

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        readonly_fields += ('created_by',)
        if obj:
            readonly_fields += ('event_rule_id',)
        return readonly_fields


class TaskAuditAdmin(admin.ModelAdmin):
    list_display = ['name', 'task_id', 'uuid', 'total_data_consumed', 'date_created']
    list_filter = ['name', 'task_id', 'uuid', 'date_created']
    date_hierarchy = 'date_created'
    change_list_template = 'admin/audit/audit_change_list.html'

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(CustomPeriodicTask, CustomPeriodicAdmin)
admin.site.register(TaskAudit, TaskAuditAdmin)
