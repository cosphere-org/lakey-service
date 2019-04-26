
from datetime import timedelta
import os


SECRET_KEY = 'not.really.needed'

DEBUG = True

#
# Lily
#
LILY_AUTHORIZER_CLASS = 'account.authorizer.Authorizer'

#
# Google OAuth2 Settings
#
GOOGLE_OAUTH2_CLIENT_ID = os.environ['GOOGLE_OAUTH2_CLIENT_ID']

GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']

GOOGLE_OAUTH2_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'

GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.profile',
]

GOOGLE_OAUTH2_USER_INFO_URI = 'https://www.googleapis.com/oauth2/v1/userinfo'

#
# AUTH REQUEST / TOKEN
#
AUTH_TOKEN_SECRET_KEY = os.environ['AUTH_TOKEN_SECRET_KEY']

AUTH_TOKEN_ALGORITHM = 'HS256'

AUTH_TOKEN_EXPIRATION_DELTA = timedelta(
    seconds=int(os.environ['AUTH_TOKEN_EXPIRATION_SECONDS']))

AUTH_REQUEST_EXPIRATION_DELTA = timedelta(
    seconds=int(os.environ['AUTH_REQUEST_EXPIRATION_SECONDS']))

#
# Internationalization
#
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


#
# Environment Dependent Common Settings
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['POSTGRES_DB'],
        'USER': os.environ['POSTGRES_USER'],
        'PASSWORD': os.environ['POSTGRES_PASSWORD'],
        'HOST': os.environ['POSTGRES_HOST'],
        'PORT': os.environ['POSTGRES_PORT'],
    },
}


#
# Templates are used by confirmation email mechanism as well as contact
# confirmation one. Also Admin part uses it for rendering of its own views.
#
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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


ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = (
    # -- lily apps
    'lily.docs',
    'lily.entrypoint',
    'lily.assertion',
    'lily.base',

    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',

    # -- service's apps
    'account',
    'catalogue',
    'downloader',
)


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
]


ROOT_URLCONF = 'conf.urls'


WSGI_APPLICATION = 'conf.wsgi.application'
