from .apps import get_app_names

from django.conf.urls import url, include

app_names = get_app_names()

urlpatterns = [url('^%s/' % app, include('.%s.urls' % app)) for app in app_names]

