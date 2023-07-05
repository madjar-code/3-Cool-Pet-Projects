from django.urls import path
from .views import (
    ContactsListView,
    ContactDetailsView,
    CreateContactView,
    CreateMultiContactsView,
    DeleteContactView,
    UpdateContactView,
    UploadContactsSheetView,
)


app_name = 'contacts'


urlpatterns = [
    path('', ContactsListView.as_view(), name='contacts_list'),
    path('create/', CreateContactView.as_view(), name='create_contact'),
    path('create-multiply/', CreateMultiContactsView.as_view(), name='create_multiply_contact'),
    path('upload-excel/', UploadContactsSheetView.as_view(), name='upload_sheet'),
    path('delete/<str:id>/', DeleteContactView.as_view(), name='delete_contact'),
    path('update/<str:id>/', UpdateContactView.as_view(), name='update_contact'),
    path('<str:id>/', ContactDetailsView.as_view(), name='contact_details'),
]
