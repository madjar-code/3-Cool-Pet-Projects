from django.contrib import admin
from common.mixins.admin import BaseAdmin
from .models import TextBlock

@admin.register(TextBlock)
class TextBlockAdmin(BaseAdmin):
    list_display = (
        'short_text',
        'author',
        'hash',
        'expiration_time',
        'is_active',
    )
    search_fields = (
        'author',
    )
    list_filter = (
        'author',
        'text',
        'is_active',
    )

    def short_text(self, obj: TextBlock) -> str:
        return obj.text[:40] + '...' if len(obj.text) > 40\
                                     else obj.text
    short_text.short_description = 'Text'
