from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from userauthentication.models import User
from userauthentication.forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active',)

    add_form = CustomUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    def save_model(self, request, obj, form, change):
        # Set is_staff to True by default when adding a new user
        obj.is_staff = True
        super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)  # Register the custom UserAdmin
