from django.db.models import Model
from .base import *


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'users.authentication.CustomJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

FLOWER_PORT = 5555
CELERY_BROKER_URL = env("CELERY_BROKER")
# CELERY_RESULT_BACKEND = env("CELERY_BACKEND")
CELERY_TIMEZONE = "Europe/Chisinau"

DATABASES = {
    'default': {
        'ENGINE': env('POSTGRES_ENGINE'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'NAME': env('MASTER_DB_NAME'),
        'HOST': env('MASTER_DB_HOST'),
        'PORT': env('MASTER_DB_PORT'),
    },

    # Docker Settings
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgres',
    #     'USER': 'postgres',
    #     'PASSWORD': 'postgres',
    #     'NAME': 'postgres',
    #     'HOST': 'database',
    #     'PORT': '5433',
    # },

    # 'replica': {
    #     'ENGINE': env('POSTGRES_ENGINE'),
    #     'USER': env('POSTGRES_USER'),
    #     'PASSWORD': env('POSTGRES_PASSWORD'),
    #     'NAME': env('REPLICA_DB_NAME'),
    #     'HOST': env('REPLICA_DB_HOST'),
    #     'PORT': env('REPLICA_DB_PORT'),
    # },
}

# USE_REPLICA_DATABASE = env('USE_REPLICA_DATABASE')

# class ReplicaRouter:
#     def db_for_read(self, model, **hints):
#         """
#         Reads go to the replica.
#         """
#         if USE_REPLICA_DATABASE:
#             return 'replica'
#         return None

#     def db_for_write(self, model, **hints):
#         """
#         Writes always go to primary.
#         """
#         return 'default'

#     def allow_relation(self, object_1: Model, object_2: Model, **hints):
#         """
#         Relations between objects are allowed if both are in the
#         primary/replica pool.
#         """
#         db_set = {'default', 'replica'}
#         if object_1._state.db in db_set and object_2._state.db in db_set:
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         return True

# DATABASE_ROUTERS=[ReplicaRouter]