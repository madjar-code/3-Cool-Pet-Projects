import os, sys, environ
import logging
import logging.config
from datetime import timedelta
from pathlib import Path
from string import ascii_letters, digits
from django.utils.log import DEFAULT_LOGGING

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = Path(__file__).parent.parent.parent

environ.Env.read_env(BASE_DIR / "server/.env")
sys.path.append(str(PROJECT_ROOT / 'apps'))

SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')
ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(' ')

DJANGO_APPS = [
    'jazzmin',    # optional
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

SITE_ID = 1

THIRD_PART_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg'
]

LOCAL_APPS = [
    'users',
    'common',
    'contacts',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PART_APPS + LOCAL_APPS


REST_USE_JWT = True

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

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

WSGI_APPLICATION = 'server.wsgi.application'

AUTH_PASSWORD_VALIDATORS = []

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=7),
}

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Chisinau'
USE_I18N = True
USE_TZ = True

# Swagger UI and OpenAPI
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'JWT': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

API_TITLE = env.str('API_TITLE')
API_VERSION = env.str('API_VERSION')
API_DESCRIPTION = env.str('API_DESCRIPTION')
API_TERMS_OF_SERVICE = env.str('API_TERMS_OF_SERVICE')
API_CONTACT_EMAIL = env.str('API_CONTACT_EMAIL')
API_LICENSE_NAME = env.str('API_LICENSE_NAME')

# Media settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Static settings
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Slug settings
SLUG_ALPHABET = ascii_letters + digits
DEFAULT_SLUG_LENGTH = 7

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

logger = logging.getLogger(__name__)

LOG_LEVEL = 'INFO'

logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
            },
            'file': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'},
            'django.server': DEFAULT_LOGGING['formatters']['django.server'],
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'formatter': 'file',
                'filename': 'logging/app.log',
            },
            'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        },
        'loggers': {
            '': {'level': 'INFO', 'handlers': ['console', 'file'], 'propagate': False},
            'apps': {'level': 'INFO', 'handlers': ['console'], 'propagate': False},
            'django.server': DEFAULT_LOGGING['loggers']['django.server'],
        }
    }
)