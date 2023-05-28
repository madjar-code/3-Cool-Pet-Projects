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
        'first_name',
        'last_name',
        'is_verified',
        'is_staff',
        'is_active',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_filter = (
        'created_at',
        'is_active',
        'is_verified',
        'is_staff',
    )
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email',
                           'username',
                           'avatar')}),
        ('Personal informations', {
            'fields': ('first_name',
                       'last_name',)
        }),
        ('Permissions', {
            'fields': ('is_verified',
                       'is_staff')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'password1',
                       'password2',
                       'description',
                       'is_active',
                       'is_staff')}
         ),
    )
    actions = (
        'activate',
        'desactivate',
        'verify',
        'unverify'
    )
    
    def activate(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_active=True)
        messages.success(request, Messages.ACTIVATE_USER.value)

    def desactivate(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_active=False)
        messages.success(request, Messages.DESACTIVATE_USER.value)

    def verify(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_verified=True)
        messages.success(request, Messages.VERIFY_USER.value)

    def unverify(modeladmin, request: HttpRequest, queryset: QuerySet) -> None:
        queryset.update(is_verified=False)
        messages.success(request, Messages.UNVERIFY_USER.value)
