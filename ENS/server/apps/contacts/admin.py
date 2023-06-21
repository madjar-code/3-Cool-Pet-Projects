from django.contrib import admin
from common.mixins.admin import BaseAdmin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(BaseAdmin):
    list_display = (
        'id',
        'name',
        'email',
        'phone',
        'priority_group',
        'created_at',
        'is_active',
    )
    list_filter = (
        'priority_group',
    )
    search_fields = (
        'name',
        'email',
        'phone',
    )
    list_display_links = (
        'id',
        'name',
    )
    model = Contact
