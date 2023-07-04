from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reports.models import NotificationSession


class SimpleNSSerializer(ModelSerializer):
    class Meta:
        model = NotificationSession
        fields = (
            'id',
            'name',
            'status',
        )
        read_only_fields = fields
