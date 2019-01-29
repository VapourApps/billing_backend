"""
Django settings for va_purchase_project project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os, braintree

try:
    import braintree_id
    import creds
except: 
    raise Exception("To use this django app, you must have a creds.py and braintree_id.py file with certain data. braintree_id needs the BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY and BRAINTREE_PRIVATE_KEY variables, and creds needs SECRET_KEY (which holds the django secret key) as well as EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL and SERVER_EMAIL variables. These are excluded from the repo for security reasons. ")

from braintree_id import BRAINTREE_MERCHANT_ID, BRAINTREE_PUBLIC_KEY, BRAINTREE_PRIVATE_KEY
from creds import SECRET_KEY

BRAINTREE_MERCHANT_ID = BRAINTREE_MERCHANT_ID or None
BRAINTREE_PUBLIC_KEY = BRAINTREE_PUBLIC_KEY or None
BRAINTREE_PRIVATE_KEY = BRAINTREE_PRIVATE_KEY or None


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY or ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*',
]

CORS_ORIGIN_WHITELIST = (
    '*', 
)

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'userprofiles',
    'silver',
    'dal',
    'dal_select2',
    'django_extensions',
    'corsheaders',
    'va_saas',
    'silver_extensions',
    'silver_cpay'
]

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_ALLOW_REFRESH': True,
#    'JWT_AUTH_HEADER_PREFIX': 'Token'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
#    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'va_saas.middleware.DisableCSRFDebug',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES' : (
        'rest_framework.renderers.JSONRenderer', 
        'rest_framework.renderers.BrowsableAPIRenderer', 
    ), 
    'DEFAULT_PERMISSION_CLASSES' : (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES' : (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',


    )
}

ROOT_URLCONF = 'va_purchase_project.urls'

PROJECT_ROOT = os.path.dirname(__file__)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_ROOT + '/payment_processors/templates/',
            PROJECT_ROOT + '/templates/',
            PROJECT_ROOT + '/silver/templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'va_purchase_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/va_billing_api/va_purchase_project/static'


#userprofiles settings


USERPROFILES_CHECK_UNIQUE_EMAIL = True


#django-silver settings

braintree_setup_data = {
    'environment': braintree.Environment.Production,
    'merchant_id': BRAINTREE_MERCHANT_ID,
    'public_key': BRAINTREE_PUBLIC_KEY,
    'private_key': BRAINTREE_PRIVATE_KEY
}

PAYMENT_PROCESSORS = {
    'braintree_triggered': {
        'class': 'silver_braintree.payment_processors.BraintreeTriggered',
        'setup_data': braintree_setup_data,
    },
    'braintree_recurring': {
        'class': 'silver_braintree.payment_processors.BraintreeTriggeredRecurring',
        'setup_data': braintree_setup_data,
    }
}

SILVER_AUTOMATICALLY_CREATE_TRANSACTIONS = True
SILVER_DOCUMENT_PREFIX = 'documents/'
SILVER_DOCUMENT_STORAGE = None
PDF_GENERATION_TIME_LIMIT = 60

TRANSACTION_SAVE_TIME_LIMIT = 5

# Email settings - for account confirmation

EMAIL_PORT = 587
EMAIL_USE_TLS = True

from creds import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL, SERVER_EMAIL

EMAIL_HOST = EMAIL_HOST or None
EMAIL_HOST_USER = EMAIL_HOST_USER or None
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD or None
DEFAULT_FROM_EMAIL = DEFAULT_FROM_EMAIL or None
SERVER_EMAIL = SERVER_EMAIL or None

# Media settings, for uploading images. 

MEDIA_ROOT = '/var/www/billing_backend/va_purchase_project/media'
MEDIA_URL = '/media/'

# VA stuff

from va_settings import *

