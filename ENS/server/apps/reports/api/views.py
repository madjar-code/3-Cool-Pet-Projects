import json
from typing import Any
from uuid import UUID
from enum import Enum
from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.request import Request
from rest_framework.response import Response
from reports.models import NotificationSession
from drf_yasg.utils import swagger_auto_schema
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


class UUIDEncoder(json.JSONEncoder):
    def default(self, object: Any):
        if isinstance(object, UUID):
            return str(object)
        return super().default(object)


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
        serializer = self.serializer_class(instance=session,
                                           context={'request': request})

        filename = 'session_report.json'
        with open(filename, 'w') as report_file:
            json.dump(serializer.data, report_file, cls=UUIDEncoder, indent=2)

        return Response(serializer.data, status.HTTP_200_OK)
