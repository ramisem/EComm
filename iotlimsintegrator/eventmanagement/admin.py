import json
from urllib.parse import quote as urlquote

from django.contrib import admin
from django.contrib import messages
from django.contrib.admin.options import IS_POPUP_VAR, TO_FIELD_VAR
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.admin.utils import (
    quote,
)
from django.forms import HiddenInput
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from masterdata.models import Event_Type_IOT_Type_Map
from .forms import EventRuleForm, EventRuleParamForm
from .models import Event_Rule_Params, Event_Rule


class Event_ActionInline(admin.StackedInline):
    model = Event_Rule_Params
    form = EventRuleParamForm
    extra = 0

    class Media:
        js = ('js/eventmanagement/maint_eventmanagement.js', 'js/util/util.js',)


class IOT_EventManagement_Admin(admin.ModelAdmin):
    list_display = ('name', 'event_type_id', 'iot_type_id', 'created_by', 'rule_frequency', 'rule_frequency_unit')
    list_filter = ['name', 'event_type_id', 'iot_type_id', 'created_by']

    inlines = [Event_ActionInline]

    change_form_template = 'admin/eventmanagement/eventmanagement_change_form.html'

    fieldsets = (
        (None, {'fields': (
            'name', 'event_type_id', 'iot_type_id', 'created_by', 'rule_frequency', 'rule_frequency_unit',
            'event_iot_map_id')}),
    )

    form = EventRuleForm

    def save_model(self, request, obj, form, change):
        try:
            map_obj = Event_Type_IOT_Type_Map.objects.get(event_type_id=obj.event_type_id,
                                                          iot_type_id=obj.iot_type_id)
            obj.event_iot_map_id = map_obj
            super().save_model(request, obj, form, change)
        except Exception as e:
            messages.error(request, f"Error saving model: {e}")
            return

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determine the HttpResponse for the add_view stage.
        """
        storage = messages.get_messages(request)
        opts = obj._meta
        preserved_filters = self.get_preserved_filters(request)
        obj_url = reverse(
            "admin:%s_%s_change" % (opts.app_label, opts.model_name),
            args=(quote(obj.pk),),
            current_app=self.admin_site.name,
        )
        # Add a link to the object's change form if the user can edit the obj.
        if self.has_change_permission(request, obj):
            obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
        else:
            obj_repr = str(obj)
        msg_dict = {
            "name": opts.verbose_name,
            "obj": obj_repr,
        }
        # Here, we distinguish between different save types by checking for
        # the presence of keys in request.POST.

        if IS_POPUP_VAR in request.POST:
            to_field = request.POST.get(TO_FIELD_VAR)
            if to_field:
                attr = str(to_field)
            else:
                attr = obj._meta.pk.attname
            value = obj.serializable_value(attr)
            popup_response_data = json.dumps(
                {
                    "value": str(value),
                    "obj": str(obj),
                }
            )
            return TemplateResponse(
                request,
                self.popup_response_template
                or [
                    "admin/%s/%s/popup_response.html"
                    % (opts.app_label, opts.model_name),
                    "admin/%s/popup_response.html" % opts.app_label,
                    "admin/popup_response.html",
                ],
                {
                    "popup_response_data": popup_response_data,
                },
            )

        elif "_continue" in request.POST or (
                # Redirecting after "Save as new".
                "_saveasnew" in request.POST
                and self.save_as_continue
                and self.has_change_permission(request, obj)
        ):
            msg = _("The {name} “{obj}” was added successfully.")
            if self.has_change_permission(request, obj):
                msg += " " + _("You may edit it again below.")
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, format_html(msg, **msg_dict), messages.SUCCESS)
            if post_url_continue is None:
                post_url_continue = obj_url
            post_url_continue = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts},
                post_url_continue,
            )
            return HttpResponseRedirect(post_url_continue)

        elif "_addanother" in request.POST:
            msg = format_html(
                _(
                    "The {name} “{obj}” was added successfully. You may add another "
                    "{name} below."
                ),
                **msg_dict,
            )
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(
                _("The {name} “{obj}” was added successfully."), **msg_dict
            )
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_add(request, obj)

    def response_change(self, request, obj):
        """
        Determine the HttpResponse for the change_view stage.
        """
        storage = messages.get_messages(request)
        if IS_POPUP_VAR in request.POST:
            opts = obj._meta
            to_field = request.POST.get(TO_FIELD_VAR)
            attr = str(to_field) if to_field else opts.pk.attname
            value = request.resolver_match.kwargs["object_id"]
            new_value = obj.serializable_value(attr)
            popup_response_data = json.dumps(
                {
                    "action": "change",
                    "value": str(value),
                    "obj": str(obj),
                    "new_value": str(new_value),
                }
            )
            return TemplateResponse(
                request,
                self.popup_response_template
                or [
                    "admin/%s/%s/popup_response.html"
                    % (opts.app_label, opts.model_name),
                    "admin/%s/popup_response.html" % opts.app_label,
                    "admin/popup_response.html",
                ],
                {
                    "popup_response_data": popup_response_data,
                },
            )

        opts = self.opts
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {
            "name": opts.verbose_name,
            "obj": format_html('<a href="{}">{}</a>', urlquote(request.path), obj),
        }
        if "_continue" in request.POST:
            msg = format_html(
                _(
                    "The {name} “{obj}” was changed successfully. You may edit it "
                    "again below."
                ),
                **msg_dict,
            )
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)

        elif "_saveasnew" in request.POST:
            msg = format_html(
                _(
                    "The {name} “{obj}” was added successfully. You may edit it again "
                    "below."
                ),
                **msg_dict,
            )
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse(
                "admin:%s_%s_change" % (opts.app_label, opts.model_name),
                args=(obj.pk,),
                current_app=self.admin_site.name,
            )
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)

        elif "_addanother" in request.POST:
            msg = format_html(
                _(
                    "The {name} “{obj}” was changed successfully. You may add another "
                    "{name} below."
                ),
                **msg_dict,
            )
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse(
                "admin:%s_%s_add" % (opts.app_label, opts.model_name),
                current_app=self.admin_site.name,
            )
            redirect_url = add_preserved_filters(
                {"preserved_filters": preserved_filters, "opts": opts}, redirect_url
            )
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(
                _("The {name} “{obj}” was changed successfully."), **msg_dict
            )
            if '(None)' not in str(obj) and len(storage._queued_messages) == 0:
                self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_change(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['event_iot_map_id'].widget = HiddenInput()
        # form.base_fields['event_rule_id'].widget = HiddenInput()
        return form

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.pk:
            param_count = Event_Rule_Params.objects.filter(event_rule_id=obj.pk).count()
            if param_count > 0:
                readonly_fields += ('iot_type_id', 'event_type_id',)
        return readonly_fields

    class Media:
        js = ('js/eventmanagement/maint_eventmanagement.js', 'js/util/util.js',)


admin.site.register(Event_Rule, IOT_EventManagement_Admin)
