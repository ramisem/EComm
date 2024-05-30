from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse


class MyAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )


my_admin_site = MyAdminSite(name="integratorconfig")
