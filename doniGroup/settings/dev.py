from .settings import *
from .constants import *

FRONT_END_HOST = 'http://localhost:3000'

MYSQL_ENGINE = 'django.db.backends.mysql'
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'doniGroup'
MYSQL_PORT = '3306'
MYSQL_USER = 'doniGroup'
MYSQL_PASSWORD = 'Giki1990????'
REDIS_HOST = ''
APP_DOMAIN = '127.0.0.1:8000'
APP_URL = 'http://localhost:8000'
CORS_ORIGIN_WHITELIST = ('localhost:8080')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

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

