from django.contrib import admin
from common.mixins.admin import ReadOnlyFieldsAdmin
from .models import NotificationState


@admin.register(NotificationState)
class NotificationStateAdmin(ReadOnlyFieldsAdmin):
    list_display = (
        'short_id',
        'contact',
        'notification_template',
        'status',
        'method',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'status',
        'method',
    )
    search_fields = (
        'contact__name',
        'notification_template__title',
        'status',
        'method',
    )
    list_display_links = (
        'short_id',
    )
    
    def short_id(self, obj):
        return str(obj.id)[:7] + '...'

    short_id.short_description = 'Short ID'

    model = NotificationState
