from django.conf import settings

HALK_ALLOWED_CURENCIES = getattr(settings, 'HALK_ALLOWED_CURENCIES', ['MKD'])