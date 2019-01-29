from django.conf.urls import url

from silver_cpay import views

urlpatterns = [
	url(r'payment-request/(?P<id>[0-9]+)', views.Cpay_View_Set.as_view({'get': 'get_payment_request'})),
	url(r'parameters', views.Cpay_View_Set.as_view({'post': 'generate_parameters'})),
	url(r'form', views.generate_cpay_form, name='cpay-form'),
	url(r'payment-success', views.Cpay_View_Set.as_view({'post': 'payment_success'}),
		name='cpay-payment-success'),
	url(r'payment-fail', views.Cpay_View_Set.as_view({'post': 'payment_fail'}),
		name='cpay-payment-fail'),
]
