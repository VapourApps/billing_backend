from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# CPAY_MERCHANT_ID is required
try:
	CPAY_MERCHANT_ID = str(getattr(settings, 'CPAY_MERCHANT_ID'))
except AttributeError:
	raise ImproperlyConfigured(
		'CPAY_MERCHANT_ID not defined in settings.py.'
		'You must define a CPAY_MERCHANT_ID in order to use the silver_cpay module'
	)

# CPAY_MERCHANT_NAME is required
try:
	CPAY_MERCHANT_NAME = str(getattr(settings, 'CPAY_MERCHANT_NAME'))
except AttributeError:
	raise ImproperlyConfigured(
		'CPAY_MERCHANT_NAME not defined in settings.py.'
		'You must define a CPAY_MERCHANT_NAME in order to use the silver_cpay module'
	)

# CPAY_PASSWORD is required
try:
	CPAY_PASSWORD = str(getattr(settings, 'CPAY_PASSWORD'))
except AttributeError:
	raise ImproperlyConfigured(
		'CPAY_PASSWORD not defined in settings.py.'
		'You must define a CPAY_PASSWORD in order to use the silver_cpay module'
	)

# CPAY_ALLOWED_CURENCIES default value
# CPAY_ALLOWED_CURENCIES = getattr(settings, 'CPAY_ALLOWED_CURENCIES', ['MKD', 'USD'])
# only MKD is allowed and harcdcoded in the code
# can not handle multiple currencies.
# to do: currency conversion to MKD

CPAY_IS_TESTING = getattr(settings, 'CPAY_IS_TESTING', False)

CPAY_IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY = getattr(settings, 'IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY', False)
