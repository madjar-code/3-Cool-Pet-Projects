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

    def render_title(self, title_data: Dict[str, str] = None) -> str:
        return self.title.format(**title_data) if title_data else self.title

    def render_text(self, text_data: Dict[str, str] = None) -> str:
        return self.text.format(**text_data) if text_data else self.title

    def __str__(self) -> str:
        return self.title if self.title else str(self.id)
