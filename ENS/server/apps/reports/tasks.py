import json
from typing import Any
from uuid import UUID
from celery import shared_task
from django.core.files.base import ContentFile
from reports.models import NotificationSession
from reports.api.serializers import (
    ReportNSSerializer,
)


class UUIDEncoder(json.JSONEncoder):
    def default(self, object: Any):
        if isinstance(object, UUID):
            return str(object)
        return super().default(object)


@shared_task(queue='default_queue')
def create_report(session_id: UUID) -> None:
    session = NotificationSession.objects.filter(id=session_id).first()
    serializer = ReportNSSerializer(instance=session)

    json_data = json.dumps(serializer.data, cls=UUIDEncoder, indent=4)
    filename = f'{session.id}.json'
    
    if session.report_file:
        session.report_file.delete(save=False)

    session.report_file.save(filename, ContentFile(json_data), save=False)
    session.save()
