from django.contrib import admin
from .models import APIDetail, HTTP_Method


class HTTP_Method_Admin(admin.ModelAdmin):
    list_display = ('method_id', 'name')
    search_fields = ('method_id', 'name',)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Add HTTP Method"
        return super().add_view(request, form_url, extra_context=extra_context)


class APIDetail_Admin(admin.ModelAdmin):
    list_display = ['api_detail_id', 'name', 'description', 'http_method', 'end_point_url']
    list_filter = ['api_detail_id', 'name']
    autocomplete_fields = ['http_method']

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Register API"
        return super().add_view(request, form_url, extra_context=extra_context)


admin.site.register(HTTP_Method, HTTP_Method_Admin)
admin.site.register(APIDetail, APIDetail_Admin)
