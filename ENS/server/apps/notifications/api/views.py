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
from notifications.models import NotificationTemplate
from notifications.utils import NotificationTokenGenerator
from .serializers import (
    NTSerializer,
    CreateNTSerializer,
)
from reports.models import (
    NotificationState,
    StatusChoices,
    MethodChoices,    
)
from notifications.utils import (
    dev_send_email,
    dev_send_email_wrong,
    dev_send_sms,
    dev_send_sms_wrong,
)
# from notifications.tasks import send_notification


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

        for contact_id in Contact.objects.values_list('id', flat=True):
            notification_template = NotificationTemplate.\
                objects.filter(id=notification_template_id).first()
            contact: Contact = Contact.objects.filter(id=contact_id).first()

            notification_state = NotificationState.objects.filter(
                notification_template=notification_template,contact=contact
            ).first()
            
            if not notification_state:
                method = None
                if contact.email:
                    method = MethodChoices.EMAIL_METHOD
                elif contact.phone:
                    method = MethodChoices.PHONE_METHOD
 
                notification_state = NotificationState.objects.create(
                    notification_template=notification_template,
                    contact=contact,
                    status=StatusChoices.STATUS_DIRTY,
                    method=method
                )
            
            if notification_state.status == StatusChoices.STATUS_DIRTY:
                subject: str = notification_template.render_title()
                body: str = notification_template.render_text()
                if notification_state.method == MethodChoices.EMAIL_METHOD:
                    contact_list: str = [contact.email]
                    try:
                        dev_send_email(subject, body, contact_list)
                        notification_state.status = StatusChoices.STATUS_READY
                    except Exception as e:
                        notification_state.status = StatusChoices.STATUS_FAILED
                    notification_state.save()

                elif notification_state.method == MethodChoices.PHONE_METHOD:
                    phone_number: str = contact.phone
                    try:
                        dev_send_sms(body, phone_number, subject)
                        notification_state.status = StatusChoices.STATUS_READY
                    except Exception as e:
                        notification_state.status = StatusChoices.STATUS_FAILED
                    notification_state.save()

        return Response({'message': 'Mass notification start'})
