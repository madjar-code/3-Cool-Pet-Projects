from django.urls import path
from .views import (
    NSessionListView,
    CreateNSessionReport,
)


app_name = 'reports'


urlpatterns = [
    path('sessions/', NSessionListView.as_view(), name='session_list'),
    path('sessions/report/<str:id>/', CreateNSessionReport.as_view(), name='create_session_report'),
]
