from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        'username', 'email', 'phone', 'region', 'favorite_cinema',
        'gender', 'birth_date',
        'is_customer', 'is_admin', 'is_staff', 'is_superuser'
    )
    list_filter = ('is_customer', 'is_admin', 'is_staff', 'gender', 'region')
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)
    list_editable = ('is_customer', 'is_admin', 'is_staff')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'email', 'first_name', 'last_name',
                'phone', 'address',
                'birth_date', 'gender',
                'region', 'favorite_cinema'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_customer', 'is_admin', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdmin)
