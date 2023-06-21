from typing import NoReturn, Union
from django.db import models
from django.utils.translation import\
    gettext_lazy as _
from django.core.exceptions import ValidationError
from phonenumber_field import modelfields
from common.mixins.models import (
    BaseModel,
)


EMPTY_FIELDS_ERROR = "At least one of the 'email' or 'phone' fields must be filled"


class PriorityChoices(models.TextChoices):
    LOW_PRIORITY = 'Low', _('Low Priority')
    HIGH_PRIORITY = 'High', _('High Priority')
    BLACKLIST = 'Blacklist', _('Blacklist')


class Contact(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True, null=True, blank=True)
    phone = modelfields.PhoneNumberField(
        max_length=30, null=True, blank=True)
    priority_group = models.CharField(
        max_length=15,
        choices=PriorityChoices.choices,
        default=PriorityChoices.LOW_PRIORITY,
    )

    def clean(self) -> Union[None, NoReturn]:
        if not self.email and not self.phone:
            raise ValidationError(EMPTY_FIELDS_ERROR)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
