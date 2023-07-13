from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from notifications.api.serializers import NTSerializer
from reports.models import (
    NotificationSession,
    NotificationState,
)


class NStateSerializer(ModelSerializer):
    class Meta:
        model = NotificationState
        fields = (
            'contact',
            'method',
            'status',
        )
        read_only_fields = fields


class ReportNSSerializer(ModelSerializer):
    notification_template = NTSerializer()
    states = NStateSerializer(many=True)
    class Meta:
        model = NotificationSession
        fields = (
            'id',
            'name',
            'status',
            'success_counter',
            'during_counter',
            'failed_counter',
            'all_counter',
            'scheduled_time',
            'created_at',
            'notification_template',
            'states',
        )
        read_only_fields = fields


class NSessionDetailsSerializer(ModelSerializer):
    notification_template = NTSerializer()
    class Meta:
        model = NotificationSession
        fields = (
            'id',
            'name',
            'status',
            'success_counter',
            'during_counter',
            'failed_counter',
            'all_counter',
            'scheduled_time',
            'created_at',
            'notification_template',
        )
        read_only_fields = fields


class SimpleNSsessionSerializer(ModelSerializer):
    class Meta:
        model = NotificationSession
        fields = (
            'id',
            'name',
            'status',
            'scheduled_time',
        )
        read_only_fields = ('status',)


class CustomNSessionSerializer(ModelSerializer):
    name = serializers.CharField(min_length=1, max_length=255)
    scheduled_time = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = NotificationSession
        fields = (
            'name',
            'scheduled_time',
        )
