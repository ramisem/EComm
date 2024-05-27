"""
URL configuration for iotlimsintegrator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

import dashboard.urls
import eventmanagement.urls

urlpatterns = [
    path('integratorconfig/', admin.site.urls),
    path('', lambda request: redirect('integratorconfig/')),
    path('eventmanagement/', include((eventmanagement.urls.URLS, 'eventmanagement'), namespace='eventmanagement')),
    path('dashboard/', include((dashboard.urls.URLS, 'dashboard'), namespace='dashboard')),
    path('admin_tools_stats/', include('admin_tools_stats.urls')),
]
