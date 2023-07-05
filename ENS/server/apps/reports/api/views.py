from enum import Enum
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from reports.models import NotificationSession
from reports.tasks import create_report
from .serializers import (
    SimpleNSsessionSerializer,
    ReportNSSerializer,
)


class ErrorMessages(str, Enum):
    NO_SESSION = 'Notification session with `id` not found'


class NSessionListView(ListAPIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = SimpleNSsessionSerializer
    queryset = NotificationSession.objects.all()

    @swagger_auto_schema(operation_id='all sessions',
                        operation_description=\
                            'Get all sessions in list')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CreateNSessionReport(RetrieveAPIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = ReportNSSerializer
    queryset = NotificationSession.objects.all()
    lookup_field = 'id'

    @swagger_auto_schema(operation_id='create_session_report')
    def get(self, request: Request, id: str) -> Response:
        session: NotificationSession = self.queryset.filter(id=id).first()
        if not session:
            return Response({'error': ErrorMessages.NO_SESSION.value},
                            status=status.HTTP_404_NOT_FOUND,)
        create_report.apply_async(args=[session.id])        

        return Response({'message': 'The report is generated!'},
                        status.HTTP_200_OK)
