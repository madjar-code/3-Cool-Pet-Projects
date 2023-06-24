from django.urls import path
from .views import (
    CreateNTView,
    StartNotificationView,
)


app_name = 'notifications'


urlpatterns = [
    path('create/', CreateNTView.as_view(), name='create_notification'),
    path('start/<str:id>/', StartNotificationView.as_view(), name='start_notification'),
]
