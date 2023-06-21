from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from contacts.models import Contact



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


class UpdateContactSerializer(ModelSerializer):
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
        read_only_fields = (
            'id',
            'created_at',
        )
