from datetime import datetime
from enum import Enum
from uuid import UUID
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
from rest_framework.serializers import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from contacts.models import Contact
from notifications.models import NotificationTemplate
from reports.models import NotificationSession
from reports.api.serializers import CustomNSessionSerializer
from notifications.utils import NotificationTokenGenerator
from .serializers import (
    NTSerializer,
    CreateNTSerializer,
)
from notifications.tasks import (
    periodic_counts,
    send_notification,
)


class ErrorMessages(str, Enum):
    NO_NOTIFICATION_TEMPLATE = 'Notification template with given `id` not found'
    NO_NOTIFICATION_SESSION = 'Notification session with given `id` not found'
    INCORRECT_SCHEDULED_TIME = 'Incorrect scheduled time'


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
    def get(self, request: Request, id: UUID) -> Response:
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


class StartNotificationView(GenericAPIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = CustomNSessionSerializer

    @swagger_auto_schema(
        operation_id='start_notification',
        operation_description='Start of notification',
    )
    def post(self, request: Request, uid: str, token: str) -> Response:
        notification_template_id = urlsafe_base64_decode(uid).decode()
        notification_template: NotificationTemplate =\
            NotificationTemplate.objects.all().\
            filter(id=notification_template_id).first()

        if not notification_template:
            return Response({'error': ErrorMessages.NO_NOTIFICATION_TEMPLATE.value},
                            status=status.HTTP_404_NOT_FOUND)

        session_serializer: CustomNSessionSerializer =\
            self.serializer_class(data=request.data)
        session_serializer.is_valid(raise_exception=True)
        session_name = session_serializer.data['name']

        scheduled_time = session_serializer.validated_data.get('scheduled_time')
        
        if scheduled_time:
            scheduled_time_object = datetime.strptime(scheduled_time, '%Y-%m-%d %H:%M:%S')
            timedelta = (scheduled_time_object - datetime.now()).total_seconds()
            response_message = f'Notification session will be started at {scheduled_time}'
        else:
            scheduled_time_object = None
            timedelta = 0
            response_message = 'Notification session started'

        notification_session = NotificationSession.objects.create(
            name=session_name,
            scheduled_time=scheduled_time_object,
            notification_template=notification_template,
        )
        session_id = notification_session.id
        
        notification_session.all_counter = Contact.objects.exclude(priority_group='Blacklist').count()
        notification_session.save()
        
        periodic_counts.apply_async(
            args=[session_id],
            # countdown=timedelta,
        )
        
        for contact_id, priority_group in Contact.objects.values_list('id', 'priority_group'):
            if priority_group in ('High', 'Low'):
                send_notification.apply_async(
                    args=[session_id, contact_id],
                    queue=f'{priority_group.lower()}_priority_queue',
                    countdown=timedelta,
                )
        return Response({'message': response_message,
                        'session': {'id': session_id,
                                    'name': session_name}},
                        status=status.HTTP_200_OK)


class RestartNotificationView(APIView)  :
    # permission_classes = (IsAdminUser,)

    @swagger_auto_schema(operation_id='restart_notification',
                         operation_description=\
                             'Restart of notification session')
    def get(self, request: Request, notification_session_id: str) -> Response:
        try:
            session_id = UUID(notification_session_id)
        except ValueError:
            raise ValidationError('Invalid notification session ID.')

        notification_session: NotificationSession =\
            NotificationSession.objects.all().\
            filter(id=notification_session_id).first()
        session_name = notification_session.name

        if not notification_session:
            return Response({'error': ErrorMessages.NO_NOTIFICATION_SESSION.value},
                            status=status.HTTP_404_NOT_FOUND)

        for contact_id, priority_group in Contact.objects.values_list('id', 'priority_group'):
            if priority_group == 'High':
                send_notification.apply_async(args=[session_id, contact_id],
                                              queue='high_priority_queue')
            elif priority_group == 'Low':
                send_notification.apply_async(args=[session_id, contact_id],
                                              queue='low_priority_queue')

        return Response({'message': 'Restart notification session',
                         'session': {'id': session_id,
                                     'name': session_name}},
                        status=status.HTTP_200_OK)