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

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self) -> str:
        return self.username

    def tokens(self) -> Tokens:
        """Return tokens for user"""
        refresh: RefreshToken = RefreshToken.for_user(self)
        return Tokens(
            refresh=str(refresh),
            access=str(refresh.access_token)
        )
