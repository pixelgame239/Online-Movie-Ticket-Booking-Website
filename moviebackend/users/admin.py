from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'is_customer', 'is_admin', 'is_superuser', 'is_active')
    list_filter = ('is_customer', 'is_admin', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'email',
                'phone', 'address', 'birth_date', 'gender', 'favorite_cinema'
            )
        }),
        ('Permissions', {
            'fields': ('is_customer', 'is_admin', 'is_superuser', 'is_active', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_customer', 'is_admin')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(User, UserAdmin)
