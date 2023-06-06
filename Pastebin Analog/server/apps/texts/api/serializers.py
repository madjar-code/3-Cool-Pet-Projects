from typing import (
    Dict,
)
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import\
    ModelSerializer

from texts.models import TextBlock



class SimpleTextBlockSerializer(ModelSerializer):
    expiration_time = serializers.DateTimeField(
        required=False, allow_null=True, format='%d.%m.%Y %H:%M:%S')
    created_at = serializers.DateTimeField(format='%d.%m.%Y')
    class Meta:
        model = TextBlock
        fields = (
            'id',
            'title',
            'author',
            'view_count',
            'expiration_time',
            'hash',
            'created_at',
        )
        read_only_fields = fields


class TextBlockSerializer(ModelSerializer):
    expiration_time = serializers.DateTimeField(
        required=False, allow_null=True, format='%d.%m.%Y %H:%M:%S')
    created_at = serializers.DateTimeField(format='%d.%m.%Y')
    class Meta:
        model = TextBlock
        fields = (
            'id',
            'title',
            'author',
            'hash',
            'text',
            'view_count',
            'expiration_time',
            'created_at',
        )
        read_only_fields = fields


class CUTextBlockSerializer(ModelSerializer):
    time_delta = serializers.IntegerField(required=False, allow_null=True)
    expiration_time = serializers.DateTimeField(
        required=False, allow_null=True,
        read_only=True, format='%Y-%m-%d %H:%M:%S')
    created_at = serializers.DateTimeField(
        read_only=True, format='%d.%m.%Y')

    class Meta:
        model = TextBlock
        fields = (
            'id',
            'title',
            'author',
            'hash',
            'text',
            'view_count',
            'expiration_time',
            'created_at',
            'time_delta',
        )
        read_only_fields = (
            'id',
            'hash',
            'author',
            'expiration_time',
            'created_at',
            'view_count',
        )
        write_only_fields = (
            'time_delta',
        )

    def _update_expiration_time(self, validated_data: Dict) -> None:
        time_delta = validated_data.pop('time_delta', None)

        if time_delta is not None:
            now = timezone.now()
            expiration_time = now + timezone.timedelta(minutes=time_delta)
            validated_data['expiration_time'] = expiration_time

    def update(self, instance: TextBlock, validated_data: Dict) -> TextBlock:
        self._update_expiration_time(validated_data)
        return super().update(instance, validated_data)

    def create(self, validated_data: Dict) -> TextBlock:
        self._update_expiration_time(validated_data)
        return super().create(validated_data)
