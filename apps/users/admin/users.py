from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.decorators import display
from unfold.forms import AdminPasswordChangeForm, UserCreationForm, UserChangeForm

from apps.users.models import User, RoleChoices


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ("telegram_id", "show_role_customized_color", "is_active")
    search_fields = ("email", "telegram_id")
    list_filter = ("role", "is_active")
    list_editable = ("is_active",)
    list_display_links = ("telegram_id",)
    fieldsets = (
        (None, {"fields": ("telegram_id", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("telegram_id", "password1", "password2"),
            },
        ),
    )

    @display(
        description=_("Role"),
        ordering="role",
        label={
            RoleChoices.ADMIN: "success",  # green
            RoleChoices.MODERATOR: "info",  # orange
            RoleChoices.USER: "info",  # red
        },
    )
    def show_role_customized_color(self, obj):
        return obj.role, obj.get_role_display()

    # @display(header=True)
    # def avatars(self, obj):
    #     return [
    #         f"{obj.first_name} {obj.last_name}",
    #         f"ID:{obj.id} - {obj.phone}",
    #         "AB",
    #         {
    #             "path": obj.avatar.url if obj.avatar else static("images/avatar.webp"),
    #             "squared": False,
    #             "borderless": True,
    #             "width": 50,
    #             "height": 50,
    #         },
    #     ]
