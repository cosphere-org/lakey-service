
from datetime import timedelta
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = 'not.really.needed'

DEBUG = True

#
# Lily
#
LILY_AUTHORIZER_CLASS = 'account.authorizer.Authorizer'

#
# LAKEY SPECIFIC
#
CATALOGUE_ITEMS_DISTRIBUTION_VALUE_LIMIT = int(
    os.environ['CATALOGUE_ITEMS_DISTRIBUTION_VALUE_LIMIT'])

CATALOGUE_ITEMS_DISTRIBUTION_VALUE_BINS_COUNT = int(
    os.environ['CATALOGUE_ITEMS_DISTRIBUTION_VALUE_BINS_COUNT'])

CATALOGUE_ITEMS_SAMPLE_SIZE = os.environ['CATALOGUE_ITEMS_SAMPLE_SIZE']

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

GOOGLE_OAUTH2_ALLOWED_DOMAINS = ['viessmann.com']

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
# AWS
#
AWS_LAKEY_REGION = os.environ['AWS_LAKEY_REGION']

AWS_LAKEY_KEY_ID = os.environ['AWS_LAKEY_KEY_ID']

AWS_LAKEY_KEY_SECRET = os.environ['AWS_LAKEY_KEY_SECRET']

AWS_LAKEY_RESULTS_LOCATION = os.environ['AWS_LAKEY_RESULTS_LOCATION']

AWS_S3_BUCKET = os.environ['AWS_S3_BUCKET']

#
# AZURE
#
AZURE_BLOB_STORAGE_ACCOUNT_NAME = os.environ['AZURE_BLOB_STORAGE_ACCOUNT_NAME']

AZURE_BLOB_STORAGE_ACCOUNT_KEY = os.environ['AZURE_BLOB_STORAGE_ACCOUNT_KEY']

AZURE_BLOB_STORAGE_CONTAINER = os.environ['AZURE_BLOB_STORAGE_CONTAINER']

#
# DATABRICKS
#
DATABRICKS_TOKEN = os.environ['DATABRICKS_TOKEN']

DATABRICKS_HOST = os.environ['DATABRICKS_HOST']

DATABRICKS_CLUSTER_ID = os.environ['DATABRICKS_CLUSTER_ID']

DATABRICKS_RESULTS_LOCATION = os.environ['DATABRICKS_RESULTS_LOCATION']

DATABRICKS_SCRIPT_LOCATION = os.environ['DATABRICKS_SCRIPT_LOCATION']


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
        'DIRS': [
            os.path.join(BASE_DIR, 'shared', 'ui', 'templates'),
            os.path.join(BASE_DIR, 'account', 'ui', 'templates'),
            os.path.join(BASE_DIR, 'catalogue', 'ui', 'templates'),
            os.path.join(BASE_DIR, 'downloader', 'ui', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'markdown': 'shared.ui.templatetags.markdown',
                'item_url': 'catalogue.ui.templatetags.item_url',
                'download_item_url': (
                    'catalogue.ui.templatetags.download_item_url'),
                'sample_table': 'catalogue.ui.templatetags.sample_table',
                'distribution_chart': (
                    'catalogue.ui.templatetags.distribution_chart'),
            }
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
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_json_widget',

    # -- service's apps
    'shared',
    'account',
    'catalogue',
    'downloader',
)


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
]

ROOT_URLCONF = 'conf.urls'


WSGI_APPLICATION = 'conf.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'shared', 'ui', 'static'),
    os.path.join(BASE_DIR, 'account', 'ui', 'static'),
]
