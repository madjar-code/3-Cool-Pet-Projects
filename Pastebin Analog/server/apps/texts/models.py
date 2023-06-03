from django.db import models
from django.db.models import Q, Manager
from django.utils import timezone
from common.mixins.models import BaseModel
from common.mixins.managers import SoftDeletionManager
from users.models import User


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
        max_length=255, blank=True, null=True)
    expiration_time = models.DateTimeField(
        null=True, blank=True, db_index=True)
    view_count = models.IntegerField(default=0)

    objects = Manager()
    active_objects = SoftDeletionManager()
    text_objects = TextBlockManager()

    class Meta:
        verbose_name = 'Text block'
        verbose_name_plural = 'Text blocks'

    def __str__(self) -> str:
        return f'Text of {self.author or "unknown user"}'

    def save(self, *args, **kwargs):
        if not self.hash:
            from texts.services.hash import HashGeneratorRandom
            hash_generator = HashGeneratorRandom()
            self.hash = hash_generator.create_unique_hash()
        super().save(*args, **kwargs)
