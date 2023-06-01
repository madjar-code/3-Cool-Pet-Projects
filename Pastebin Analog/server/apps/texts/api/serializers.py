from typing import (
    Dict,
    Optional,
)
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import\
    ModelSerializer

from users.models import User
from texts.models import TextBlock



class SimpleTextBlockSerializer(ModelSerializer):
    expiration_time = serializers.SerializerMethodField(
        required=False, allow_null=True)
    class Meta:
        model = TextBlock
        fields = (
            'id',
            'author',
            'expiration_time',
            'hash',
        )
        read_only_fields = fields

    def get_expiration_time(self, obj: TextBlock) -> Optional[str]:
        expiration_time = obj.expiration_time
        if expiration_time is not None:
            formatted_datetime = expiration_time.\
                strftime('%Y-%m-%d %H:%M:%S')
            return formatted_datetime
        return None


class TextBlockSerializer(ModelSerializer):
    expiration_time = serializers.SerializerMethodField(
        required=False, allow_null=True)
    class Meta:
        model = TextBlock
        fields = (
            'id',
            'author',
            'hash',
            'text',
            'expiration_time',
        )
        read_only_fields = fields

    def get_expiration_time(self, obj: TextBlock) -> Optional[str]:
        expiration_time = obj.expiration_time
        if expiration_time is not None:
            formatted_datetime = expiration_time.\
                strftime('%Y-%m-%d %H:%M:%S')
            return formatted_datetime
        return None


class CUTextBlockSerializer(ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True)
    time_delta = serializers.IntegerField(required=False, allow_null=True)
    expiration_time = serializers.SerializerMethodField(
        required=False, allow_null=True)

    class Meta:
        model = TextBlock
        fields = (
            'id',
            'author',
            'hash',
            'text',
            'expiration_time',
            'time_delta',
        )
        read_only_fields = (
            'id',
            'hash',
        )
        write_only_fields = (
            'time_delta',
        )

    def get_expiration_time(self, obj: TextBlock) -> Optional[str]:
        expiration_time = obj.expiration_time
        if expiration_time is not None:
            formatted_datetime = expiration_time.\
                strftime('%Y-%m-%d %H:%M:%S')
            return formatted_datetime
        return None

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
