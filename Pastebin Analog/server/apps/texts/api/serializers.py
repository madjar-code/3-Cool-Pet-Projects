from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import\
    ModelSerializer

from users.models import User
from texts.models import TextBlock


class SimpleTextBlockSerializer(ModelSerializer):
    class Meta:
        model = TextBlock
        fields = (
            'id',
            'author',
            'hash',
        )
        read_only_fields = fields


class TextBlockSerializer(ModelSerializer):
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


class CreateTextBlockSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True)
    expiration_time = serializers.SerializerMethodField(required=False, allow_null=True)
    time_delta = serializers.IntegerField(required=False, allow_null=True)

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

    def get_expiration_time(self, obj):
        expiration_time = obj.expiration_time
        if expiration_time is not None:
            # Форматирование даты и времени в удобочитаемый формат
            formatted_datetime = expiration_time.strftime('%Y-%m-%d %H:%M:%S')
            return formatted_datetime
        return None

    def create(self, validated_data):
        time_delta = validated_data.pop('time_delta', None)

        if time_delta is not None:
            now = timezone.now()
            expiration_time = now + timezone.timedelta(minutes=time_delta)
            validated_data['expiration_time'] = expiration_time

        return super().create(validated_data)
