"""va_purchase_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin

from custom_apps.urls import urlpatterns as custom_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^silver/', include('silver.urls')),
    url(r'^va_saas/', include('va_saas.urls')),
    url(r'^va_silver/', include('silver_extensions.urls')),
    url(r'^va_silver/cpay/', include('silver_cpay.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += custom_urlpatterns
