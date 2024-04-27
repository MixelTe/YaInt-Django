from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users import models

fieldsets = UserAdmin.fieldsets
fieldsets[1][1]["fields"] = fieldsets[1][1]["fields"] + (
    "image",
    "image_tmb",
    "trusted",
)
fieldsets[3][1]["fields"] = fieldsets[3][1]["fields"] + (
    "attempts_count",
    "deactivation_date",
)


@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = fieldsets
    readonly_fields = ["image_tmb"]


__all__ = []
