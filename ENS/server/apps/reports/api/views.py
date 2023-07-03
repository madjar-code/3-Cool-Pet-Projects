from rest_framework.permissions import (
    IsAdminUser,
)
from rest_framework.generics import (
    ListAPIView,
)
from reports.models import NotificationSession
from drf_yasg.utils import swagger_auto_schema
from .serializers import SimpleNSSerializer

class NSListView(ListAPIView):
    # permission_classes = (IsAdminUser,)
    serializer_class = SimpleNSSerializer
    queryset = NotificationSession.objects.all()

    @swagger_auto_schema(operation_id='all sessions',
                        operation_description=\
                            'Get all sessions in list')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
