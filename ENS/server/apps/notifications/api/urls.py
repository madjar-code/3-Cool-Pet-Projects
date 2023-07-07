from django.urls import path
from .views import (
    CreateNTView,
    NTListView,
    SendNotificationTokenView,
    StartNotificationView,
    RestartNotificationView
)


app_name = 'notifications'


urlpatterns = [
    path('', NTListView.as_view(), name='notifications_list'),
    path('create/', CreateNTView.as_view(), name='create_notification'),
    path('start/token/<str:id>/', SendNotificationTokenView.as_view(), name='notification_token'),
    path('start/<str:uid>/<str:token>/<str:session_name>/', StartNotificationView.as_view(), name='start_notification'),
    path('restart/<str:notification_session_id>/', RestartNotificationView.as_view(), name='restart_notification'),
]
