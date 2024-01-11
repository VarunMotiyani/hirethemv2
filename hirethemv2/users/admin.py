from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from hirethemv2.users.forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email", "phone_number",  "urn_number", "profile_picture", "bio", "address")}),
        (_("Education info"), {"fields": ("tenth_percentage", "tenth_school_name", "twelth_percentage", "twelth_school_name")}),
        (_("Other info"), {"fields": ("current_cgpa", "active_backlogs")}),
        (_("Github"), {"fields": ("github", "department")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = ["username", "email", "name", "is_superuser"]
    search_fields = ["name", "email"]
