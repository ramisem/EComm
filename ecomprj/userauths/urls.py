from django.urls import path
from userauths import views

app_name = 'userauths'


class URLS:
    urlpatterns = [
        path("sign-up/", views.register_view, name='sign-up'),
        path("sign-in/", views.login_view, name='sign-in'),
        path("sign-out/<str:email>/", views.logout_view_with_param, name='sign-out'),
    ]

    def __dir__(self) :
        return self.urlpatterns
