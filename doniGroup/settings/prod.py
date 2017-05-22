from .settings import *
from .constants import *

FRONT_END_HOST = 'http://app.tramodity.com'

MYSQL_ENGINE = 'django.db.backends.mysql'
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'tramodity'
MYSQL_PORT = '3306'
MYSQL_USER = 'tramodity'
MYSQL_PASSWORD = 'Giki1990????'
REDIS_HOST = ''

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APP_URL = 'http://app.tramodity.com'
CORS_ORIGIN_WHITELIST = (APP_URL, )

CSRF_TRUSTED_ORIGINS = (
    APP_URL,
)

CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)

DATABASES = {
    # 'default': {
    #     'NAME': 'my_database',
    #     'ENGINE': 'sqlserver_ado',
    #     'HOST': 'donigroup.cczhghwibti9.us-west-2.rds.amazonaws.com:1433 ',
    #     'USER': 'immadimtiaz',
    #     'PASSWORD': 'Giki1990????',
    # }

    'default': {
        'ENGINE': MYSQL_ENGINE,
        'NAME': MYSQL_DB,
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PORT,
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PASSWORD,
    }
}