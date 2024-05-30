from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin
from import_export.formats import base_formats

from iotlimsintegrator.views import my_admin_site
from userauthentication.models import User
from .forms import API_Property_Details_Form, API_Detail_Form
from .models import APIDetail, ApplicationDetail, API_Property_Details
from .resources import ApplicationDetailResource, APIDetailResource


class ApplicationDetail_Admin(ImportExportActionModelAdmin):
    list_display = ('name', 'base_url', 'created_dt', 'created_by')
    list_filter = ['name', 'created_dt', 'created_by']
    resource_classes = [ApplicationDetailResource]

    change_form_template = 'admin/change_form.html'

    fieldsets = (
        (None, {
            'fields': ('name', 'base_url',),
            'classes': ('extrapretty', 'wide'),
        }),
    )

    date_hierarchy = 'created_dt'

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Add Application Details"
        return super().add_view(request, form_url, extra_context=extra_context)

    def get_import_formats(self):
        formats = (
            base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]

    def save_model(self, request, obj, form, change):
        try:
            if request.user.is_authenticated:
                username = request.user.username
                user_map_obj = User.objects.get(username=username)
                obj.created_by = user_map_obj
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error saving model: {e}")
            return


class APIDetail_ActionInline(admin.StackedInline):
    model = API_Property_Details
    extra = 0

    form = API_Property_Details_Form


class APIDetail_Admin(ImportExportActionModelAdmin):
    list_display = ['name', 'app_id', 'description', 'end_point_url', 'type', 'created_dt', 'created_by']
    list_filter = ['name', 'app_id', 'type', 'created_dt', 'created_by']

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'app_id', 'end_point_url', 'success_code', 'authorization_property_id',
                       'authorization_keyword', 'type',),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Processing Script'), {
            'fields': ('processing_script',),
            'classes': ('extrapretty', 'wide'),
        }),
    )

    resource_classes = [APIDetailResource]

    change_form_template = 'admin/change_form.html'

    form = API_Detail_Form

    date_hierarchy = 'created_dt'

    inlines = [APIDetail_ActionInline]

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Register API"
        return super().add_view(request, form_url, extra_context=extra_context)

    def get_import_formats(self):
        formats = (
            base_formats.CSV,
        )
        return [f for f in formats if f().can_export()]

    def save_model(self, request, obj, form, change):
        try:
            if request.user.is_authenticated:
                username = request.user.username
                user_map_obj = User.objects.get(username=username)
                obj.created_by = user_map_obj
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error saving model: {e}")
            return


my_admin_site.register(ApplicationDetail, ApplicationDetail_Admin)
my_admin_site.register(APIDetail, APIDetail_Admin)
