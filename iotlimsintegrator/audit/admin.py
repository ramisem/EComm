from auditlog.admin import LogEntryAdmin
from auditlog.models import LogEntry
from django.contrib import admin


class CustomLogEntryAdmin(LogEntryAdmin):

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save'] = False
        extra_context['show_save_as_new'] = False
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        extra_context['show_delete_link'] = False
        extra_context['original'] = False
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    change_form_template = 'admin/audit/audit_change_form.html'


admin.site.unregister(LogEntry)
admin.site.register(LogEntry, CustomLogEntryAdmin)
