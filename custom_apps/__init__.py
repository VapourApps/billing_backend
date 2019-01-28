import os, django

from django.conf.urls import url, include

script_path = os.path.dirname(os.path.realpath(__file__))

INSTALLED_APPS = [f for f in os.listdir(script_path) if os.path.isdir(os.path.join(script_path,f))]

urlpatterns = []

try:
    urlpatterns = [url('^%s/' % app, include('custom_apps.%s.urls' % app)) for app in INSTALLED_APPS]
except Exception: 
    print ('Something wrong with patterns')
    import traceback
    traceback.print_exc()
    pass

INSTALLED_APPS = ['custom_apps.' + x for x in INSTALLED_APPS]


