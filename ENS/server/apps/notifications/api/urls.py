from django.urls import path
from .views import (
    CreateNTView,
    SendNotificationTokenView,
    StartNotificationView,
)


app_name = 'notifications'


urlpatterns = [
    path('create/', CreateNTView.as_view(), name='create_notification'),
    path('start/token/<str:id>/', SendNotificationTokenView.as_view(), name='notification_token'),
    path('start/<str:uid>/<str:token>/', StartNotificationView.as_view(), name='start_notification'),
]
