from django.urls import path
from .views import (
    ContactsListView,
)


app_name = 'contacts'


urlpatterns = [
    path('', ContactsListView.as_view(), name='contacts_list'),
]
