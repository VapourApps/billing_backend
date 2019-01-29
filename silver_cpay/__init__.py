from django.conf import settings

CPAY_ALLOWED_CURENCIES = getattr(settings, 'CPAY_ALLOWED_CURENCIES', ['MKD'])