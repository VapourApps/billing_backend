from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'get_plans', views.get_plans),
    url(r'get_customers', views.get_customers),
    url(r'get_subscriptions', views.get_subscriptions),
    url(r'edit_customer', views.edit_customer),
]
