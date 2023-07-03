from django.db import models
from common.mixins.models import (
    UUIDModel,
    TimeStampModel,
)
from contacts.models import Contact
from notifications.models import NotificationTemplate


class NotificationSession(UUIDModel):
    name = models.CharField(max_length=255)
    notification_template = models.ForeignKey(
        to=NotificationTemplate, on_delete=models.CASCADE,
        related_name='sessions')

    def __str__(self) -> str:
        return self.name


class StatusChoices(models.TextChoices):
    STATUS_DIRTY = 'DIRTY', 'DIRTY'
    STATUS_DURING = 'DURING', 'DURING'
    STATUS_READY = 'READY', 'READY'
    STATUS_FAILED = 'FAILED', 'FAILED'


class MethodChoices(models.TextChoices):
    EMAIL_METHOD = 'EMAIL', 'EMAIL'
    PHONE_METHOD = 'PHONE', 'PHONE'


class NotificationState(UUIDModel, TimeStampModel):
    contact = models.ForeignKey(
        to=Contact, on_delete=models.CASCADE,
        related_name='states')
    notification_session = models.ForeignKey(
        to=NotificationSession, on_delete=models.CASCADE,
        related_name='states', blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices,
        default=StatusChoices.STATUS_DIRTY)
    method = models.CharField(
        max_length=10, choices=MethodChoices.choices)

    def __str__(self) -> str:
        return f'{self.notification_session} to'\
               f' {self.contact}'
