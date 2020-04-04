
from datetime import timedelta
import os


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
    # 'django.contrib.admin',
    'material.admin',
    'material.admin.default',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'rest_framework',

    # -- service's apps
    'account',
    'catalogue',
    'downloader',
)


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]


ROOT_URLCONF = 'conf.urls'


WSGI_APPLICATION = 'conf.wsgi.application'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

MATERIAL_ADMIN_SITE = {
    'HEADER':  ('Lakey-service admin panel'),  # Admin site header
    'TITLE':  ('Lakey-service'),  # Admin site title
    # 'FAVICON':  'path/to/favicon',  # Admin site favicon (path to static should be specified)
    # 'MAIN_BG_COLOR':  'black',  # Admin site main color, css color should be specified
    # 'MAIN_HOVER_COLOR':  'red',  # Admin site main hover color, css color should be specified
    # 'PROFILE_PICTURE':  'path/to/image',  # Admin site profile picture (path to static should be specified)
    # 'PROFILE_BG':  'path/to/image',  # Admin site profile background (path to static should be specified)
    # 'LOGIN_LOGO':  'path/to/image',  # Admin site logo on login page (path to static should be specified)
    # 'LOGOUT_BG':  'path/to/image',  # Admin site background on login/logout pages (path to static should be specified)
    'SHOW_THEMES':  True,  #  Show default admin themes button
    'TRAY_REVERSE': False,  # Hide object-tools and additional-submit-line by default
    'NAVBAR_REVERSE': False,  # Hide side navbar by default
    'SHOW_COUNTS': True, # Show instances counts for each model
    # 'APP_ICONS': {  # Set icons for applications(lowercase), including 3rd party apps, {'application_name': 'material_icon_name', ...}
    #     'sites': 'send',
    # },
    # 'MODEL_ICONS': {  # Set icons for models(lowercase), including 3rd party models, {'model_name': 'material_icon_name', ...}
    #     'site': 'contact_mail',
    # }
}