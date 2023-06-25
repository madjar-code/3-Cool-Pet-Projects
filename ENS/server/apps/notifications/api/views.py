from datetime import datetime
from enum import Enum
from django.utils.http import (
    urlsafe_base64_encode,
    urlsafe_base64_decode,
)
from django.utils.encoding import force_bytes
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    GenericAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from contacts.models import Contact
from reports.models import (
    MethodChoices,
    StatusChoices,
    NotificationState,
)
from notifications.models import NotificationTemplate
from notifications.utils import (
    NotificationTokenGenerator,
    dev_send_email,
    dev_send_email_wrong,
)
from .serializers import (
    NTSerializer,
    CreateNTSerializer,
)


class ErrorMessages(str, Enum):
    NO_NOTIFICATION_TEMPLATE = 'Notification template with given `id` not found'


class CreateNTView(CreateAPIView):
    serializer_class = CreateNTSerializer
    # permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='create_notification_template')
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data.pop('ignore_typos', None)  # Remove the ignore_typos field
        instance = serializer.create(data)
        serializer = self.serializer_class(instance)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SendNotificationTokenView(GenericAPIView):
    serializer_class = NTSerializer
    # permission_classes = (IsAdminUser,)
    queryset = NotificationTemplate.objects.all()

    @swagger_auto_schema(operation_id='notification_token',
                         operation_description=\
                             'Generates notification start token')
    def get(self, request: Request, id: str) -> Response:
        notification_template: NotificationTemplate =\
            self.queryset.filter(id=id).first()

        if not notification_template:
            return Response({'error': ErrorMessages.NO_NOTIFICATION_TEMPLATE.value},
                            status=status.HTTP_404_NOT_FOUND,)

        timestamp: float = datetime.now().timestamp()
        uid = urlsafe_base64_encode(force_bytes(notification_template.id))
        token = NotificationTokenGenerator().make_token(notification_template, timestamp)

        serializer = self.serializer_class(notification_template)
        return Response({'notification': serializer.data,
                         'uid': uid, 'token': token}, status.HTTP_200_OK)


class NTListView(ListAPIView):
    serializer_class = NTSerializer
    # permission_classes = (IsAdminUser,)
    queryset = NotificationTemplate.objects.all()

    @swagger_auto_schema(operation_id='all_contacts')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class StartNotificationView(APIView):
    # permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='start_notification',
                         operation_description=\
                             'Confirmation of notification')
    def get(self, request: Request, uid: str, token: str) -> Response:
        notification_template_id = urlsafe_base64_decode(uid).decode()
        notification_template: NotificationTemplate =\
            NotificationTemplate.objects.all().\
            filter(id=notification_template_id).first()

        if not notification_template:
            return Response({'error': ErrorMessages.NO_NOTIFICATION_TEMPLATE.value},
                            status=status.HTTP_404_NOT_FOUND)

        for contact in Contact.objects.all():
            notification_state = NotificationState.objects.create(
                notification_template=notification_template,
                contact=contact,
                status=StatusChoices.STATUS_DIRTY,
                method=MethodChoices.EMAIL_METHOD,
            )
            subject: str = notification_template.render_title()
            body: str = notification_template.render_text()
            contact_list: str = [contact.email]
            dev_send_email(subject, body, contact_list)

        return Response({'message': 'Mass notification start'})
