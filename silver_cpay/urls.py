from django.conf.urls import url

from silver_cpay import views

urlpatterns = [
	url(r'payment_request/(?P<id>[0-9]+)', views.Cpay_View_Set.as_view({'get': 'get_payment_request'})),
	#url(r'payment_request', views.Cpay_View_Set.as_view({'get': 'get_payment_requests'})),
	#url(r'notification', views.Cpay_View_Set.as_view({'get': 'get_notifications'})),
	url(r'parameters', views.Cpay_View_Set.as_view({'post': 'generate_parameters'})),
	url(r'form', views.generate_cpay_form, name='cpay-form'),
	url(r'payment_success', views.Cpay_View_Set.as_view({'post': 'payment_success'}),
		name='cpay-payment-success'),
	url(r'payment_fail', views.Cpay_View_Set.as_view({'post': 'payment_fail'}),
		name='cpay-payment-fail'),
]
