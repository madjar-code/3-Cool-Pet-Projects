from django.contrib import admin
from common.mixins.admin import ReadOnlyFieldsAdmin
from .models import (
    NotificationSession,
    NotificationState,
)


@admin.register(NotificationSession)
class NotificationSessionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'success_counter',
        'during_counter',
        'failed_counter',
        'all_counter',
        'status',
        'scheduled_time',
        'created_at',
        'notification_template',
    )
    readonly_fields = (
        'success_counter',
        'during_counter',
        'failed_counter',
        'all_counter',
        'created_at',
    )
    list_filter = (
        'name',
        'status',
    )
    search_fields = (
        'notification_template__title',
    )
    list_display_links = (
        'id',
        'name',
    )
    

@admin.register(NotificationState)
class NotificationStateAdmin(ReadOnlyFieldsAdmin):
    list_display = (
        'short_id',
        'contact',
        'notification_session',
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
        'notification_session__name',
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
