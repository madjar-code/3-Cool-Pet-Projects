import random
from django.db import models
from django.conf import settings
from common.mixins.models import BaseModel
from users.models import User


def _create_hash() -> str:
    letters: str = settings.HASH_ALPHABET
    length: int = settings.DEFAULT_HASH_LENGTH
    random_hash: str = ''.join(random.choice(letters)\
                               for _ in range(length))
    return random_hash


class TextBlock(BaseModel):
    text = models.TextField(max_length=2096)
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, blank=True, null=True)
    hash = models.CharField(
        max_length=settings.DEFAULT_HASH_LENGTH,
        default=_create_hash, unique=True)

    class Meta:
        verbose_name = 'Text block'
        verbose_name_plural = 'Text blocks'

    def __str__(self) -> str:
        if self.author:
            return f'Text of {self.author}'
        return f'Text of unknown user'
