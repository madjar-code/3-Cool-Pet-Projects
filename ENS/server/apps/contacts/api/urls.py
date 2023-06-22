from django.urls import path
from .views import (
    ContactsListView,
    ContactDetailsView,
    CreateContactView,
    UploadContactsSheetView,
)


app_name = 'contacts'


urlpatterns = [
    path('', ContactsListView.as_view(), name='contacts_list'),
    path('create/', CreateContactView.as_view(), name='create_contact'),
    path('upload-excel/', UploadContactsSheetView.as_view(), name='upload_sheet'),
    path('<str:id>/', ContactDetailsView.as_view(), name='contact_details'),
]
