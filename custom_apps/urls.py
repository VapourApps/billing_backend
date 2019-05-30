from .apps import get_app_names

from django.conf.urls import url, include

import importlib

app_names = get_app_names()
urlpatterns = [url('^%s/' % app, include('custom_apps.%s.urls' % app)) for app in app_names]

