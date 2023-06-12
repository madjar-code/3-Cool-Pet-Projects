from typing import Optional
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token) -> Optional[User]:
        user = super().get_user(validated_token)

        if user is None:
            pass

        return user
