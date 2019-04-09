from django.conf.urls import url

from silver_halk import views

urlpatterns = [
	url(r'payment_request/(?P<id>[0-9]+)', views.Halk_View_Set.as_view({'get': 'get_payment_request'})),
	#url(r'payment_request', views.Halk_View_Set.as_view({'get': 'get_payment_requests'})),
	#url(r'notification', views.Halk_View_Set.as_view({'get': 'get_notifications'})),
	url(r'parameters', views.Halk_View_Set.as_view({'post': 'generate_parameters'})),
	url(r'form', views.generate_halk_form, name='halk-form'),
	url(r'payment_success', views.Halk_View_Set.as_view({'post': 'payment_success'}),
		name='halk-payment-success'),
	url(r'payment_fail', views.Halk_View_Set.as_view({'post': 'payment_fail'}),
		name='halk-payment-fail'),
]
