from django.contrib import admin

from .models import Event_Type, Event_Type_IOT_Type_Map, Param, Unit, EventRuleParams


# Register your models here.

class Event_Type_IOT_Type_Map_Inline(admin.StackedInline):
    model = Event_Type_IOT_Type_Map
    fields = ('iot_type_id',)
    extra = 0


class Event_Type_Custom_Admin(admin.ModelAdmin):
    list_display = ['event_name', 'description']
    search_fields = ['event_name']
    inlines = [Event_Type_IOT_Type_Map_Inline]
    fieldsets = (
        (None, {'fields': ('event_name', 'description'), 'classes': ('wide',)}),
    )


admin.site.register(Event_Type, Event_Type_Custom_Admin)


class Param_Admin(admin.ModelAdmin):
    list_display = ['param_name', 'vendor_param_id', 'description', 'unit']
    search_fields = ['param_name', 'vendor_param_id']


admin.site.register(Param, Param_Admin)


class Unit_Admin(admin.ModelAdmin):
    list_display = ['unit_name']
    search_fields = ['unit_name']


admin.site.register(Unit, Unit_Admin)


class Event_Rule_Param_Inline(admin.TabularInline):
    model = EventRuleParams
    fields = ('paramid',)
    extra = 0


class Event_Type_IOT_Type_Map_Admin(admin.ModelAdmin):
    list_display = ['event_type_id', 'iot_type_id']
    readonly_fields = ['event_type_id', 'iot_type_id']
    list_filter = ['event_type_id', 'iot_type_id']

    inlines = [Event_Rule_Param_Inline]

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Event_Type_IOT_Type_Map, Event_Type_IOT_Type_Map_Admin)
