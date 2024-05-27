from django.contrib import admin, messages

from refenrencetype.models import ReferenceType, RefValues
from userauthentication.models import User


class RefValuesInline(admin.TabularInline):
    model = RefValues
    fields = (
        "value",
        "display_value",
    )
    extra = 0


@admin.register(ReferenceType)
class ReferenceTypeAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                ),
            },
        ),
    )
    list_display = (
        "name",
        "description",
        "created_dt",
        "created_by",
    )
    list_filter = [
        "name",
    ]
    date_hierarchy = 'created_dt'
    inlines = [RefValuesInline]

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
