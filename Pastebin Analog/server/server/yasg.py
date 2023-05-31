from django.conf import settings
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


API_TITLE = settings.API_TITLE
API_VERSION = settings.API_VERSION
API_DESCRIPTION = settings.API_DESCRIPTION
API_TERMS_OF_SERVICE = settings.API_TERMS_OF_SERVICE
API_CONTACT_EMAIL = settings.API_CONTACT_EMAIL
API_LICENSE_NAME = settings.API_LICENSE_NAME

info = openapi.Info(
    title=API_TITLE,
    default_version=API_VERSION,
    description=API_DESCRIPTION,
    terms_of_service=API_TERMS_OF_SERVICE,
    contact=openapi.Contact(email=API_CONTACT_EMAIL),
    license=openapi.License(name=API_LICENSE_NAME),
)
