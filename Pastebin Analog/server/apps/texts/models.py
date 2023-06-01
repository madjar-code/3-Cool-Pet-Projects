import secrets
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from common.mixins.models import BaseModel
from common.mixins.managers import SoftDeletionManager
from users.models import User


def _create_hash() -> str:
    letters: str = settings.HASH_ALPHABET
    length: int = settings.DEFAULT_HASH_LENGTH
    random_hash: str = ''.join(secrets.choice(letters) for _ in range(length))
    return random_hash


class TextBlockManager(SoftDeletionManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            Q(expiration_time__gt=timezone.now()) |
            Q(expiration_time__isnull=True))


class TextBlock(BaseModel):
    text = models.TextField(max_length=2096)
    author = models.ForeignKey(
        to=User, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='text_blocks')
    hash = models.CharField(
        max_length=settings.DEFAULT_HASH_LENGTH,
        default=_create_hash, unique=True)
    expiration_time = models.DateTimeField(
        null=True, blank=True, db_index=True)

    objects = SoftDeletionManager()
    text_objects = TextBlockManager()

    class Meta:
        verbose_name = 'Text block'
        verbose_name_plural = 'Text blocks'

    def __str__(self) -> str:
        return f'Text of {self.author or "unknown user"}'
