from typing import NamedTuple
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    AccessToken
)
from common.mixins.models import UUIDModel
from .managers import UserManager


class Tokens(NamedTuple):
    refresh: RefreshToken
    access: AccessToken


class User(UUIDModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(
        max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars', default='avatars/default.png'
    )
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')

    def __str__(self) -> str:
        return self.email

    def tokens(self) -> Tokens:
        """Return tokens for user"""
        refresh: RefreshToken = RefreshToken.for_user(self)
        return Tokens(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )
