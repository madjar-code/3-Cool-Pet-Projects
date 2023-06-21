from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from contacts.models import Contact
from .serializers import (
    SimpleContactSerializer,
    ContactSerializer,
    UpdateContactSerializer,
    CreateContactSerializer,
)



class ContactsListView(ListAPIView):
    serializer_class = SimpleContactSerializer
    permission_classes = (IsAdminUser,)

    queryset = Contact.active_objects.all()

    @swagger_auto_schema(operation_id='all_text_blocks')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
