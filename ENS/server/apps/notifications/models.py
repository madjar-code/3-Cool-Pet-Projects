from typing import Dict
from django.db import models
from common.mixins.models import (
    UUIDModel,
)


class NotificationTemplate(UUIDModel):
    send_time = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now=True)

    def render_title(self, title_data: Dict[str, str]) -> str:
        return self.title.format(**title_data)

    def render_text(self, text_data: Dict[str, str]) -> str:
        return self.text.format(**text_data)

    def __str__(self) -> str:
        return self.title if self.title else str(self.id)
