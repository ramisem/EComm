from django.urls import path

from utils import views

app_name = 'utils'


class URLS:
    urlpatterns = [
        path("command/", views.command, name='command'),
    ]

    def __dir__(self):
        return self.urlpatterns
