from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import IOT_Type, IOT_Device


class IOT_Type_Admin(admin.ModelAdmin):
    list_display = ('iot_type_id', 'description')
    search_fields = ('iot_type_id', 'description',)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Add IOT Type"
        return super().add_view(request, form_url, extra_context=extra_context)

    def history_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['history_entry_list'] = LogEntry.objects.filter(object_id=object_id)
        return super().history_view(request, object_id, extra_context)


class IOT_Device_Admin(admin.ModelAdmin):
    list_display = ('iot_device_id', 'name', 'iot_type_id', 'serialnumber', 'externalid', 'uuid')
    search_fields = ('iot_device_id', 'name', 'serialnumber', 'externalid', 'uuid', 'iot_type_id__description')
    actions = ['sync_device_info', ]
    autocomplete_fields = ['iot_type_id']

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Add IOT Device"
        return super().add_view(request, form_url, extra_context=extra_context)

    def history_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        extra_context['history_entry_list'] = LogEntry.objects.filter(object_id=object_id)
        print('extra_context', LogEntry.objects.filter(object_id=object_id))
        return super().history_view(request, object_id, extra_context)

    def sync_device_info(self, request, queryset):
        pass

    sync_device_info.short_description = "Sync Device Info"


admin.site.register(IOT_Type, IOT_Type_Admin)
admin.site.register(IOT_Device, IOT_Device_Admin)
