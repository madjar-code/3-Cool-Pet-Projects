from rest_framework import serializers
from rest_framework.serializers import\
    ModelSerializer

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
        )
        read_only_fields = fields
