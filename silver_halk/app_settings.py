from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# CPAY_MERCHANT_ID is required
try:
	HALK_STORE_KEY = str(getattr(settings, 'HALK_STORE_KEY'))
except AttributeError:
	raise ImproperlyConfigured(
		'HALK_STORE_KEY not defined in settings.py.'
		'You must define a HALK_STORE_KEY in order to use the silver_halk module'
	)

# CPAY_MERCHANT_NAME is required
try:
	HALK_CLIENT_ID = str(getattr(settings, 'HALK_CLIENT_ID'))
except AttributeError:
	raise ImproperlyConfigured(
		'HALK_CLIENT_ID not defined in settings.py.'
		'You must define a HALK_CLIENT_ID in order to use the silver_halk module'
	)

HALK_ALLOWED_CURENCIES = ['MKD']

HALK_IS_TESTING = getattr(settings, 'HALK_IS_TESTING', True)

HALK_IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY = getattr(settings, 'IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY', False)
