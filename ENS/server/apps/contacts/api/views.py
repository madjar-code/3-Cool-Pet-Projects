from enum import Enum
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAdminUser
from drf_yasg.utils import swagger_auto_schema
from contacts.models import Contact
from .serializers import (
    SimpleContactSerializer,
    ContactSerializer,
    UpdateContactSerializer,
    CreateContactSerializer,
)

class ErrorMessages(str, Enum):
    NO_USER = 'User with `username` not found'
    NO_CONTACT = 'Contact with `id` not found'


class ContactsListView(ListAPIView):
    serializer_class = SimpleContactSerializer
    # permission_classes = (IsAdminUser,)

    queryset = Contact.active_objects.all()

    @swagger_auto_schema(operation_id='all_contacts')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ContactDetailsView(RetrieveAPIView):
    serializer_class = ContactSerializer
    # permission_classes = (IsAdminUser,)
    queryset = Contact.active_objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(operation_id='contact_details')
    def get(self, request: Request, id: str) -> Response:
        contact: Contact = self.queryset.filter(id=id).first()
        if not contact:
            return Response({'error': ErrorMessages.NO_CONTACT.value},
                            status=status.HTTP_404_NOT_FOUND,)
        serializer = self.serializer_class(instance=contact)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateContactView(CreateAPIView):
    serializer_class = CreateContactSerializer
    # permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='create_contact')
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

