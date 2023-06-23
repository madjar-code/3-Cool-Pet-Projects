from rest_framework.serializers import ModelSerializer
from notifications.models import NotificationTemplate


class CreateNTSerializer(ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = (
            'id',
            'send_time',
            'title',
            'text',
            'created_at'
        )
        read_only_fields = (
            'id',
            'created_at',
        )
