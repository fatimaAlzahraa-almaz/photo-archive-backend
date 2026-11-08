from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserAdminCreationForm, UserAdminChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = (
        "email",
        "name",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "is_staff",
        "is_active",
        "is_superuser",
    )

    search_fields = ("email", "name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "name",
                "password1",
                "password2",
            ),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")