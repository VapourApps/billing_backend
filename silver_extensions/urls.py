from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'get_plans', views.get_plans),
    url(r'get_customers', views.get_customers),
    url(r'get_subscriptions', views.get_subscriptions),
    url(r'edit_customer', views.edit_customer),

    url(r'halk_pay_select', views.halk_pay_select),
    url(r'halk_pay_confirm', views.halk_pay_confirm, name='halk-pay-confirm'),
    url(r'halk_payment_ok/(?P<halk_request_id>[0-9]+)', views.halk_payment_ok),
    url(r'halk_payment_ok', views.halk_payment_ok, name='halk-pay-ok'),
    url(r'halk_payment_fail/(?P<halk_request_id>[0-9]+)', views.halk_payment_fail,),
    url(r'halk_payment_fail', views.halk_payment_fail, name='halk-pay-fail'),

    url(r'pay_select/(?P<invoice_series>\d*)$', views.pay_select),
#   url(r'pay_select/(?P<invoice_series>\d+)$', views.pay_select_url),
    url(r'pay_confirm', views.pay_confirm, name='pay-confirm'),
    url(r'cpay_payment_ok/(?P<cpay_request_id>[0-9]+)', views.cpay_payment_ok),
    url(r'cpay_payment_ok', views.cpay_payment_ok, name='pay-ok'),
    url(r'cpay_payment_fail/(?P<cpay_request_id>[0-9]+)', views.cpay_payment_fail,),
    url(r'cpay_payment_fail', views.cpay_payment_fail, name='pay-fail'),


    
]
