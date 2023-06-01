from enum import Enum
from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http.request import HttpRequest
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from common.mixins.admin import ReadOnlyFieldsAdmin
from .models import User

admin.site.unregister(Group)


class Messages(str, Enum):
    ACTIVATE_USER = 'Selected User(s) are now activate!'
    DESACTIVATE_USER = 'Selected User(s) are now desactivate!'
    VERIFY_USER = 'Selected User(s) are now verified!'
    UNVERIFY_USER = 'Selected User(s) are now unverified!'


@admin.register(User)
class UserAdmin(UserAdmin,
                ReadOnlyFieldsAdmin):
    list_display = (
        'username',
        'email',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'created_at',
        'is_active',
        'is_staff',
    )
    ordering = ('-created_at',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'is_active',
                       'is_staff')}
         ),
    )
    actions = (
        'activate',
        'desactivate',
    )
    
    def activate(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_active=True)
        messages.success(request, Messages.ACTIVATE_USER.value)

    def desactivate(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_active=False)
        messages.success(request, Messages.DESACTIVATE_USER.value)
