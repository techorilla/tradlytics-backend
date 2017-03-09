"""
Django settings for doniGroup project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from os.path import abspath, dirname
import djcelery

from .constants import *

# from doniCore.middleware.session_expiry import SessionExpiry

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DJANGO_ROOT = dirname(dirname(dirname(abspath(__file__))))
PROJECT_ROOT = os.path.join(dirname(DJANGO_ROOT), 'doniGroup')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=^5p6c(@(e#^w!v_0cvwnfh11bwng6@dltr!z-ujdifxrm5eh3'



ALLOWED_HOSTS = ['tramodity.com', 'donigroup.com', 'localhost', '.tramodity']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    # Application Apps

    'doniServer',
    'emailApp',
    'website',

    # Third Party Application
    'grappelli',
    'jsoneditor',
    'ckeditor',
    'easy_thumbnails',
    'djcelery',
    'markdownx',
    'django_countries'

]

# For django-countries all flag icon urls
COUNTRIES_FLAG_URL = 'flags/1x1/{code}.svg'

COUNTRIES_OVERRIDE = {
    ('RK', 'Russia / Ukraine'),
    ('EU', 'European Union'),
}

#CKE EDITOR TEXT EDITOR FOR DJANGO ADMIN
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
CKEDITOR_UPLOAD_PATH = os.path.join(PROJECT_ROOT, "website", 'static', 'blog'),

# Admin JSON editor
JSON_EDITOR_JS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/4.2.1/jsoneditor.js'
JSON_EDITOR_CSS = 'https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/4.2.1/jsoneditor.css'

'''
Celery Related Variables
'''
# CELERY BROKER IP
BROKER_INTERNAL_IP = '127.0.0.1'
# Broker settings.
BROKER_PORT = 6379
BROKER_URL = "redis://%s:%s//" % (BROKER_INTERNAL_IP, BROKER_PORT)
# Using the database to store task state and results.
CELERY_RESULT_BACKEND = "redis://%s:%s/" % (BROKER_INTERNAL_IP, BROKER_PORT)
CELERY_RESULT_DBURI = "redis://%s:%s/0" % (BROKER_INTERNAL_IP, BROKER_PORT)
CELERYD_MAX_TASKS_PER_CHILD = 4
CELERY_REDIRECT_STDOUTS_LEVEL = 'ERROR'
CELERY_TRACK_STARTED = True

djcelery.setup_loader()



MIDDLEWARE = [
    'doniServer.middleware.SessionExpiry',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# Authentication Backend
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'doniGroup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT,'website', 'templates')],
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

WSGI_APPLICATION = 'doniGroup.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

IS_HTTPS = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, "website", 'static'),
)

CONTACT_US_EMAIL_TEMPLATE = '%s/emailApp/templates/contact_us.tpl' % PROJECT_ROOT
BASE_EMAIL_TEMPLATE = '%s/emailApp/templates/base_email.tpl' % PROJECT_ROOT
EMAIL_ASSETS = "%s/emailApp/static/img/assets/" % DJANGO_ROOT

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'immadimtiaz@gmail.com'
EMAIL_INFO = ['immadimtiaz@gmail.com']


from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + thumbnail_settings.THUMBNAIL_PROCESSORS