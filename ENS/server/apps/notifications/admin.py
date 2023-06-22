from django.contrib import admin
from .models import NotificationTemplate


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'text',
        'send_time',
    )
    list_filter = (
        'created_at',
    )
    search_fields = (
        'title',
        'text',
        'send_time',
    )
    list_display_links = (
        'id',
        'title',
    )
    model = NotificationTemplate
