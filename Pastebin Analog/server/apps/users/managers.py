from enum import Enum
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import User


class ErrorMessages(str, Enum):
    NO_USERNAME = 'User needs to have an username'
    NO_EMAIL = 'User needs to have and email'
    NO_PASSWORD = 'User needs to have a password'


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str) -> User:
        if not username:
            raise ValueError(ErrorMessages.NO_USERNAME.value)
        if not email:
            raise ValueError(ErrorMessages.NO_EMAIL.value)
        if not password:
            raise ValueError(ErrorMessages.NO_PASSWORD.value)

        email: str = self.normalize_email(email)
        user: User = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, email: str, password: str) -> User:
        user: User = self.create_user(
            username=username, email=self.normalize_email(email),
            password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
