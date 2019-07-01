
import os

from .settings import *  # noqa


INSTALLED_APPS += (  # noqa
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_admin_json_editor',
)


MIDDLEWARE += [  # noqa
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]


ROOT_URLCONF = 'conf.urls_admin'


WSGI_APPLICATION = 'conf.wsgi_admin.application'


STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'STATIC')
