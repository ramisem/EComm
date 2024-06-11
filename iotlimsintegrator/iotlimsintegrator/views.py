from django.conf import settings
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse

from refenrencetype.models import RefValues


class MyAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)

        required_reftype_id = getattr(settings, 'APPLICATION_MODULE_IMAGES_REF_NO', '-1')
        module_images = RefValues.objects.filter(reftype_id=int(required_reftype_id)).values_list('value',
                                                                                                  'display_value')
        module_images_dict = {value: display_value for value, display_value in module_images}

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
            'module_images': module_images_dict,
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )


my_admin_site = MyAdminSite(name="integratorconfig")
