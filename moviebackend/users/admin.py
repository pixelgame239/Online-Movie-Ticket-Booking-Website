from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Các field hiển thị trong list
    list_display = ("username", "email", "is_customer", "is_superuser")
    list_filter = ("is_customer", "is_superuser")

    # Form khi edit user
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Thông tin cá nhân", {"fields": ("first_name", "last_name", "email", "phone", "address", "birth_date", "gender", "favorite_cinema")}),
        ("Phân quyền", {"fields": ("is_customer", "is_active",  "is_superuser", "groups", "user_permissions")}),
        ("Thời gian", {"fields": ("last_login", "date_joined")}),
    )

    # Form khi tạo user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "is_customer",  "is_superuser"),
        }),
    )

    search_fields = ("username", "email")
    ordering = ("username",)

admin.site.register(User, UserAdmin)
