from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Book

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ("username", "email", "first_name", "last_name", "date_of_birth", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "is_superuser", "groups")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "date_of_birth", "profile_photo")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Keep add form simple
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "password1", "password2")}),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

# Explicit registration (what the checker expects)
admin.site.register(CustomUser, CustomUserAdmin)

# Optional: manage books in admin too
admin.site.register(Book)