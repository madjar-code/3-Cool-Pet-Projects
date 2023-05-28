from enum import Enum
from django.contrib import admin, messages
from django.http.request import HttpRequest
from django.db.models import QuerySet


class Messages(str, Enum):
    DELETE_COMPLETE = 'Selected entities are deleted'
    RESTORE_COMPLETE = 'Selected entities are restored'


class ReadOnlyFieldsAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id',
        'created_at',
        'updated_at',
    )


class SoftDeletionAdmin(admin.ModelAdmin):
    actions = (
        'soft_delete',
        'restore',
    )
    
    def soft_delete(self, request: HttpRequest,
                    queryset: QuerySet) -> None:
        queryset.update(is_active=False)
        messages.success(
            request, Messages.DELETE_COMPLETE.value)

    def restore(self, request: HttpRequest,
                    queryset: QuerySet) -> None:
        queryset.update(is_active=True)
        messages.success(
            request, Messages.RESTORE_COMPLETE)

    soft_delete.short_description = 'Soft Deletion'
    restore.short_description = 'Restoring'


class BaseAdmin(ReadOnlyFieldsAdmin,
                SoftDeletionAdmin):
    pass
