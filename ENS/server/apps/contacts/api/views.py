import os
from enum import Enum
from django.core.files import File
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import (
    MultiPartParser,
)
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from contacts.models import Contact
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from .serializers import (
    SimpleContactSerializer,
    ContactSerializer,
    UpdateContactSerializer,
    CreateContactSerializer,
)


class ErrorMessages(str, Enum):
    NO_USER = 'User with `username` not found'
    NO_CONTACT = 'Contact with `id` not found'
    INVALID_TYPE = 'Invalid file type. Only Excel files (.xlsx) are supported.'


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


class DeleteContactView(DestroyAPIView):
    serializer_class = SimpleContactSerializer
    queryset = Contact.active_objects.all()
    lookup_field = 'id'
    
    @swagger_auto_schema(operation_id='delete_contact')
    def delete(self, reuqest: Request, id: str) -> Response:
        contact: Contact = self.queryset.filter(id=id).first()
        if not contact:
            return Response({'error': ErrorMessages.NO_CONTACT.value},
                            status=status.HTTP_404_NOT_FOUND)
        contact.soft_delete()
        return Response({'message': 'Deletion complete!'},
                        status=status.HTTP_204_NO_CONTENT)


class UpdateContactView(GenericAPIView):
    serializer_class = UpdateContactSerializer
    queryset = Contact.active_objects.all()
    # permission_classes  = (IsAdminUser,)

    @swagger_auto_schema(operation_id='update_contact')
    def put(self, request: Request, id: str) -> Response:
        contact: Contact = self.queryset.filter(id=id).first()
        if not contact:
            return Response({'error': ErrorMessages.NO_CONTACT.value},
                            status=status.HTTP_404_NOT_FOUND)

        serialilizer = self.serializer_class(
            instance=contact, data=request.data, partial=True)
        serialilizer.is_valid(raise_exception=True)
        serialilizer.save()
        return Response(serialilizer.data, status=status.HTTP_200_OK)


class UploadContactsSheetView(APIView):
    parser_classes = (MultiPartParser,)
    serializer_class = None

    @swagger_auto_schema(
        operation_id='upload_sheet',
        manual_parameters=[
            openapi.Parameter(
                'file',
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description='Excel sheet file'
            ),
        ]
    )
    def post(self, request: Request) -> Response:
        file_object: File = request.data['file']
        file_name = file_object.name
        file_extension = os.path.splitext(file_name)[1].lower()

        if file_extension != '.xlsx':
            return Response({'error': ErrorMessages.INVALID_TYPE.value},
                            status=status.HTTP_400_BAD_REQUEST)

        wb = load_workbook(file_object)
        sheet: Worksheet = wb.active
        contacts = []
        errors = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, email, phone, priority_group = row

            contact_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'priority_group': priority_group,
            }

            serializer = CreateContactSerializer(data=contact_data)
            if serializer.is_valid():
                serializer.save()
                contacts.append(serializer.data)
            else:
                errors.append(serializer.errors)

        return Response({'contacts': contacts, 'errors': errors}, status=status.HTTP_200_OK)