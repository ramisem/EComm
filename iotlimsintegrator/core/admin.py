import requests
from django.conf import settings
from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import helpers
from django.contrib.admin.options import csrf_protect_m, IncorrectLookupParameters
from django.contrib.admin.utils import (
    model_ngettext,
)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import (
    PermissionDenied,
)
from django.db import router, transaction
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseBase
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.utils.translation import gettext as _
from django.utils.translation import ngettext

from apidetails.models import ApplicationDetail
from userauthentication.models import User
from .models import IOT_Type, IOT_Device


class IOT_Type_Admin(admin.ModelAdmin):
    list_display = ('model_name',)
    search_fields = ('model_name',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('model_id', 'model_name', 'description'),
        }),
    )

    fieldsets = (
        (None, {'fields': ('model_id', 'model_name',)}),
    )

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Add IOT Type"
        return super().add_view(request, form_url, extra_context=extra_context)


class IOT_Device_Admin(admin.ModelAdmin):
    list_display = ('uuid', 'iot_type_id', 'name', 'serialnumber', 'externalid', 'created_dt', 'created_by')
    search_fields = ('name', 'serialnumber', 'externalid', 'uuid', 'iot_type_id__model_name')
    actions = ['sync_device_info', 'sync_individual_device_info']
    autocomplete_fields = ['iot_type_id']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('iot_type_id', 'uuid', 'name', 'serialnumber', 'externalid', 'description', 'manufacturer'),
        }),
    )

    fieldsets = (
        (
            None,
            {'fields': ('iot_type_id', 'uuid', 'name', 'serialnumber', 'externalid', 'description', 'manufacturer')}),
    )

    date_hierarchy = 'created_dt'

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['add_title'] = "Add IOT Device"
        return super().add_view(request, form_url, extra_context=extra_context)

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

    def sync_device_info(self, request, queryset):
        iot_application_name = getattr(settings, 'APPLICATION_IOT_DEVICE_APP_NAME', '')
        iot_device_info_api = getattr(settings, 'APPLICATION_GET_ALL_IOT_DEVICE_INFO_API', '')
        iot_device_info_api_token_property = getattr(settings, 'APPLICATION_IOT_DEVICE_INFO_API_TOKEN_PROPERTY', '')
        iot_device_info_api_token_id = getattr(settings, 'APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID', '')

        disputed_property = ''

        if iot_application_name == '':
            disputed_property += 'APPLICATION_IOT_DEVICE_APP_NAME'
        if iot_device_info_api == '':
            disputed_property += ',APPLICATION_GET_ALL_IOT_DEVICE_INFO_API'
        if iot_device_info_api_token_property == '':
            disputed_property += ',APPLICATION_IOT_DEVICE_INFO_API_TOKEN_PROPERTY'
        if iot_device_info_api_token_id == '':
            disputed_property += ',APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID'

        if disputed_property != '':
            if disputed_property.startswith(','):
                disputed_property = disputed_property[1:]  # Remove the leading comma
            self.message_user(request,
                              f"System configuration is not correct, Please check the following properties in the settings file: {disputed_property}")
            return

        iot_application_info = ApplicationDetail.objects.filter(name=iot_application_name).values(
            'base_url').first()

        if iot_application_info:
            base_url = iot_application_info['base_url']
            api_url = base_url + iot_device_info_api + '?' + iot_device_info_api_token_property + '=' + iot_device_info_api_token_id

            response = requests.get(api_url)

            if response.status_code == 200:
                all_devices = response.json()

                for device in all_devices:
                    device_filter_kwargs = {'uuid': device['uuid']}
                    device_defaults = {
                        'name': device['name'],
                        'serialnumber': device['machine']['serial_number'],
                        'externalid': device['machine']['mac_address'],
                        'description': device['description'],
                        'uuid': device['uuid'],
                        'iot_type_id': IOT_Type.objects.update_or_create(model_id=device['machine']['machine_model_id'],
                                                                         defaults={
                                                                             'model_name': device['machine']['model']})[
                            0]
                    }
                    # Use update_or_create for IOT_Device
                    IOT_Device.objects.update_or_create(
                        **device_filter_kwargs,
                        defaults=device_defaults
                    )

                self.message_user(request, "API call successful.")
            else:
                self.message_user(request, "API call failed.")
        else:
            self.message_user(request,
                              "No record found for the IOT device. Please check the APPLICATION_IOT_DEVICE_APP_NAME property in the setting file.")

    def sync_individual_device_info(self, request, queryset):
        with transaction.atomic():
            api_call_failed = False
            iot_application_name = getattr(settings, 'APPLICATION_IOT_DEVICE_APP_NAME', '')
            iot_device_info_api = getattr(settings, 'APPLICATION_INDIVIDUAL_IOT_DEVICE_INFO_API', '')
            iot_device_info_api_token_property = getattr(settings, 'APPLICATION_IOT_DEVICE_INFO_API_TOKEN_PROPERTY', '')
            iot_device_info_api_token_id = getattr(settings, 'APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID', '')

            disputed_property = ''

            if iot_application_name == '':
                disputed_property += 'APPLICATION_IOT_DEVICE_APP_NAME'
            if iot_device_info_api == '':
                disputed_property += ',APPLICATION_INDIVIDUAL_IOT_DEVICE_INFO_API'
            if iot_device_info_api_token_property == '':
                disputed_property += ',APPLICATION_IOT_DEVICE_INFO_API_TOKEN_PROPERTY'
            if iot_device_info_api_token_id == '':
                disputed_property += ',APPLICATION_IOT_DEVICE_INFO_API_TOKEN_ID'

            if disputed_property != '':
                if disputed_property.startswith(','):
                    disputed_property = disputed_property[1:]  # Remove the leading comma
                self.message_user(request,
                                  f"System configuration is not correct, Please check the following properties in the settings file: {disputed_property}")
                return

            iot_application_info = ApplicationDetail.objects.filter(name=iot_application_name).values(
                'base_url').first()

            if not iot_application_info:
                raise Exception(
                    "No record found for the IOT device. Please check the APPLICATION_IOT_DEVICE_APP_NAME property in the setting file.")

            base_url = iot_application_info['base_url']

            for device in queryset:
                try:
                    device_filter_kwargs = {'uuid': device.uuid}
                    iot_device_info_api = iot_device_info_api.replace("[device.uuid]", device.uuid)
                    api_url = base_url + iot_device_info_api + "?" + iot_device_info_api_token_property + "=" + iot_device_info_api_token_id
                    response = requests.get(api_url)
                    if response.status_code == 200:
                        devices_info = response.json()
                        device_defaults = {
                            'name': devices_info['name'],
                            'serialnumber': devices_info['machine']['serial_number'],
                            'externalid': devices_info['machine']['mac_address'],
                            'description': devices_info['description'],
                            'iot_type_id':
                                IOT_Type.objects.update_or_create(model_id=devices_info['machine']['machine_model_id'],
                                                                  defaults={
                                                                      'model_name': devices_info['machine']['model']})[
                                    0]
                        }
                        # Use update_or_create for IOT_Device
                        IOT_Device.objects.update_or_create(
                            **device_filter_kwargs,
                            defaults=device_defaults
                        )
                    else:
                        self.message_user(request, "API call failed.")
                        api_call_failed = True
                        break
                except requests.exceptions.RequestException as e:
                    raise Exception(f"API call failed for device['uuid'], aborting. Error: {e}")

        if not api_call_failed:
            self.message_user(request, "API call successful.")

    sync_device_info.short_description = "Sync Device Info(For All)"
    sync_individual_device_info.short_description = "Sync Device Info(For Individual Device)"

    def response_action(self, request, queryset):
        """
        Handle an admin action. This is called if a request is POSTed to the
        changelist; it returns an HttpResponse if the action was handled, and
        None otherwise.
        """

        # There can be multiple action forms on the page (at the top
        # and bottom of the change list, for example). Get the action
        # whose button was pushed.
        try:
            action_index = int(request.POST.get("index", 0))
        except ValueError:
            action_index = 0

        # Construct the action form.
        data = request.POST.copy()
        data.pop(helpers.ACTION_CHECKBOX_NAME, None)
        data.pop("index", None)

        # Use the action whose button was pushed
        try:
            data.update({"action": data.getlist("action")[action_index]})
        except IndexError:
            # If we didn't get an action from the chosen form that's invalid
            # POST data, so by deleting action it'll fail the validation check
            # below. So no need to do anything here
            pass

        action_form = self.action_form(data, auto_id=None)
        action_form.fields["action"].choices = self.get_action_choices(request)

        # If the form's valid we can handle the action.
        if action_form.is_valid():
            action = action_form.cleaned_data["action"]
            select_across = action_form.cleaned_data["select_across"]
            func = self.get_actions(request)[action][0]

            # Get the list of selected PKs. If nothing's selected, we can't
            # perform an action on it, so bail. Except we want to perform
            # the action explicitly on all objects.
            selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
            if request.POST['action'] == 'sync_device_info':
                ct = ContentType.objects.get_for_model(queryset.model)
                queryset = ct.model_class().objects.first()
                select_across = True
            elif not selected and not select_across:
                # Reminder that something needs to be selected or nothing will happen
                msg = _(
                    "Items must be selected in order to perform "
                    "actions on them. No items have been changed."
                )
                self.message_user(request, msg, messages.WARNING)
                return None

            if not select_across:
                # Perform the action only on the selected objects
                queryset = queryset.filter(pk__in=selected)

            response = func(self, request, queryset)

            # Actions may return an HttpResponse-like object, which will be
            # used as the response from the POST. If not, we'll be a good
            # little HTTP citizen and redirect back to the changelist page.
            if isinstance(response, HttpResponseBase):
                return response
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            msg = _("No action selected.")
            self.message_user(request, msg, messages.WARNING)
            return None

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        """
        The 'change list' admin view for this model.
        """
        from django.contrib.admin.views.main import ERROR_FLAG

        app_label = self.opts.app_label
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied

        try:
            cl = self.get_changelist_instance(request)
        except IncorrectLookupParameters:
            # Wacky lookup parameters were given, so redirect to the main
            # changelist page, without parameters, and pass an 'invalid=1'
            # parameter via the query string. If wacky parameters were given
            # and the 'invalid=1' parameter was already in the query string,
            # something is screwed up with the database, so display an error
            # page.
            if ERROR_FLAG in request.GET:
                return SimpleTemplateResponse(
                    "admin/invalid_setup.html",
                    {
                        "title": _("Database error"),
                    },
                )
            return HttpResponseRedirect(request.path + "?" + ERROR_FLAG + "=1")

        # If the request was POSTed, this might be a bulk action or a bulk
        # edit. Try to look up an action or confirmation first, but if this
        # isn't an action the POST will fall through to the bulk edit check,
        # below.
        action_failed = False
        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        actions = self.get_actions(request)
        # Actions with no confirmation
        if (
                actions
                and request.method == "POST"
                and "index" in request.POST
                and "_save" not in request.POST
        ):
            if selected:
                response = self.response_action(
                    request, queryset=cl.get_queryset(request)
                )
                if response:
                    return response
                else:
                    action_failed = True
            elif request.POST['action'] in 'sync_device_info':
                response = self.response_action(
                    request, queryset=cl.get_queryset(request)
                )
                if response:
                    return response
            else:
                msg = _(
                    "Items must be selected in order to perform "
                    "actions on them. No items have been changed."
                )
                self.message_user(request, msg, messages.WARNING)
                action_failed = True

        # Actions with confirmation
        if (
                actions
                and request.method == "POST"
                and helpers.ACTION_CHECKBOX_NAME in request.POST
                and "index" not in request.POST
                and "_save" not in request.POST
        ):
            if selected:
                response = self.response_action(
                    request, queryset=cl.get_queryset(request)
                )
                if response:
                    return response
                else:
                    action_failed = True

        if action_failed:
            # Redirect back to the changelist page to avoid resubmitting the
            # form if the user refreshes the browser or uses the "No, take
            # me back" button on the action confirmation page.
            return HttpResponseRedirect(request.get_full_path())

        # If we're allowing changelist editing, we need to construct a formset
        # for the changelist given all the fields to be edited. Then we'll
        # use the formset to validate/process POSTed data.
        formset = cl.formset = None

        # Handle POSTed bulk-edit data.
        if request.method == "POST" and cl.list_editable and "_save" in request.POST:
            if not self.has_change_permission(request):
                raise PermissionDenied
            FormSet = self.get_changelist_formset(request)
            modified_objects = self._get_list_editable_queryset(
                request, FormSet.get_default_prefix()
            )
            formset = cl.formset = FormSet(
                request.POST, request.FILES, queryset=modified_objects
            )
            if formset.is_valid():
                changecount = 0
                with transaction.atomic(using=router.db_for_write(self.model)):
                    for form in formset.forms:
                        if form.has_changed():
                            obj = self.save_form(request, form, change=True)
                            self.save_model(request, obj, form, change=True)
                            self.save_related(request, form, formsets=[], change=True)
                            change_msg = self.construct_change_message(
                                request, form, None
                            )
                            self.log_change(request, obj, change_msg)
                            changecount += 1
                if changecount:
                    msg = ngettext(
                        "%(count)s %(name)s was changed successfully.",
                        "%(count)s %(name)s were changed successfully.",
                        changecount,
                    ) % {
                              "count": changecount,
                              "name": model_ngettext(self.opts, changecount),
                          }
                    self.message_user(request, msg, messages.SUCCESS)

                return HttpResponseRedirect(request.get_full_path())

        # Handle GET -- construct a formset for display.
        elif cl.list_editable and self.has_change_permission(request):
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(queryset=cl.result_list)

        # Build the list of media to be used by the formset.
        if formset:
            media = self.media + formset.media
        else:
            media = self.media

        # Build the action form and populate it with available actions.
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields["action"].choices = self.get_action_choices(request)
            media += action_form.media
        else:
            action_form = None

        selection_note_all = ngettext(
            "%(total_count)s selected", "All %(total_count)s selected", cl.result_count
        )

        context = {
            **self.admin_site.each_context(request),
            "module_name": str(self.opts.verbose_name_plural),
            "selection_note": _("0 of %(cnt)s selected") % {"cnt": len(cl.result_list)},
            "selection_note_all": selection_note_all % {"total_count": cl.result_count},
            "title": cl.title,
            "subtitle": None,
            "is_popup": cl.is_popup,
            "to_field": cl.to_field,
            "cl": cl,
            "media": media,
            "has_add_permission": self.has_add_permission(request),
            "opts": cl.opts,
            "action_form": action_form,
            "actions_on_top": self.actions_on_top,
            "actions_on_bottom": self.actions_on_bottom,
            "actions_selection_counter": self.actions_selection_counter,
            "preserved_filters": self.get_preserved_filters(request),
            **(extra_context or {}),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_list_template
            or [
                "admin/%s/%s/change_list.html" % (app_label, self.opts.model_name),
                "admin/%s/change_list.html" % app_label,
                "admin/change_list.html",
            ],
            context,
        )


admin.site.register(IOT_Type, IOT_Type_Admin)
admin.site.register(IOT_Device, IOT_Device_Admin)
