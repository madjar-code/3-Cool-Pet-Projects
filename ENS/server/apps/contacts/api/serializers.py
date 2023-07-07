from typing import (
    Dict,
    Any,
)
from enum import Enum
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from contacts.models import Contact


class ErrorMessages(str, Enum):
    NO_PHONE_AND_EMAIL = "Either 'phone' or 'email' field is required."


class SimpleContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'priority_group',
        )
        read_only_fields = fields


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'priority_group',
            'created_at',
            'is_active',
        )
        read_only_fields = fields


class CreateContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'priority_group',
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if 'phone' not in attrs and 'email' not in attrs:
            raise ValidationError(ErrorMessages.NO_PHONE_AND_EMAIL.value)
        return attrs


class UpdateContactSerializer(ModelSerializer):
    name = serializers.CharField(required=False)
    class Meta:
        model = Contact
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'priority_group',
            'created_at',
        )
        read_only_fields = (
            'id',
            'created_at',
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        if 'phone' in attrs and not attrs['phone']:
            if not self.instance.email:
                raise ValidationError(ErrorMessages.NO_PHONE_AND_EMAIL.value)
        if 'email' in attrs and not attrs['email']:
            if not self.instance.phone:
                raise ValidationError(ErrorMessages.NO_PHONE_AND_EMAIL.value)

        if 'phone' in attrs and 'email' in attrs:
            if not attrs['phone'] and not attrs['email']:
                raise ValidationError(ErrorMessages.NO_PHONE_AND_EMAIL.value)
        return attrs
