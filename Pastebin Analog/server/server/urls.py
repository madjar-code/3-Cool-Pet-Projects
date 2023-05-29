from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import \
    TokenRefreshView,\
    TokenObtainPairView
from .yasg import schema_view


API_PREFIX = 'api/v1'

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Apps
    path(f'{API_PREFIX}/text-blocks/', include('texts.api.urls')),
    path(f'{API_PREFIX}/users/', include('users.api.urls')),

    # Tokens
    path(f'{API_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{API_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# API Docs
urlpatterns += [
    path('swagger<str:format>/', schema_view.without_ui(), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc'), name='schema-redoc'),
]
