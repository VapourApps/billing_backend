from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'get_plans', views.get_plans),
    url(r'get_customers', views.get_customers),
    url(r'get_subscriptions', views.get_subscriptions),
    url(r'edit_customer', views.edit_customer),
    url(r'pay_select/(?P<invoice_series>\d*)$', views.pay_select),
#    url(r'pay_select/(?P<invoice_series>\d+)$', views.pay_select_url),
    url(r'pay_confirm', views.pay_confirm, name='pay-confirm'),
    url(r'cpay_payment_ok/(?P<cpay_request_id>[0-9]+)', views.cpay_payment_ok),
    url(r'cpay_payment_ok', views.cpay_payment_ok, name='pay-ok'),
    url(r'cpay_payment_fail/(?P<cpay_request_id>[0-9]+)', views.cpay_payment_fail,),
    url(r'cpay_payment_fail', views.cpay_payment_fail, name='pay-fail'),
    url(r'add_billing_log', views.add_new_billing_log, name = 'add_billing_log'),

    #NOTE this may be placed in a separate app in the future
    url(r'update_subscription_status', views.change_subscription_status, name = 'change_subscription_status'),
]
