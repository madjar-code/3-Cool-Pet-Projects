from enum import Enum
from typing import Dict, Any
from django.contrib import auth
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError,
)
from rest_framework.exceptions import\
    AuthenticationFailed
from users.models import User


class Messages(str, Enum):
    EMAIL_TAKEN = 'This email is already taken'
    PASSWORD_MISMATCH = 'The entered passwords do not match'
    INVALID_LOGIN = 'Incorrect email or password'
    ACCOUNT_DISABLED = 'Account disabled, contact admin'


class RegisterSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        min_length=5, max_length=68, write_only=True)
    confirm_password = serializers.CharField(
        min_length=5, max_length=68, write_only=True, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'confirm_password',
        )

    def validate_email(self, value: str) -> str:
        email: str = self.get_initial().get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(Messages.EMAIL_TAKEN.value)
        return value

    def validate_confirm_password(self, value: str) -> str:
        password: str = self.get_initial().get('password')
        confirm_password: str = self.get_initial().get('confirm_password')

        if password != confirm_password:
            raise ValidationError(Messages.PASSWORD_MISMATCH.value)
        return value

    def create(self, validated_data: Dict) -> User:
        password: str = validated_data.pop('password', None)
        del validated_data['confirm_password']
        user: User = self.Meta.model(**validated_data)
    
        if password:
            user.set_password(password)
        user.save()
        return user


class LoginSerializer(ModelSerializer):
    email = serializers.EmailField(
        min_length=3, max_length=255, write_only=True)
    password = serializers.CharField(
        min_length=5, max_length=68, write_only=True)
    access = serializers.CharField(
        min_length=6, max_length=68, read_only=True)
    refresh = serializers.CharField(
        min_length=6, max_length=68, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'access',
            'refresh',
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        email: str = attrs.get('email', '')
        password: str = attrs.get('password', '')

        user: User = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(Messages.INVALID_LOGIN.value)
        if not user.is_active:
            raise AuthenticationFailed(Messages.ACCOUNT_DISABLED.value)

        return user.tokens()._asdict()
