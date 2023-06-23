from django.urls import path
from .views import (
    CreateNTView,
)


app_name = 'notifications'


urlpatterns = [
    path('create/', CreateNTView.as_view(), name='create_notification'),
]
