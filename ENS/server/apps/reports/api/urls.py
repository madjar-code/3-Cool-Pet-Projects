from django.urls import path
from .views import NSListView


app_name = 'reports'


urlpatterns = [
    path('sessions/', NSListView.as_view(), name='session_list'),
]
