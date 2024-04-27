from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class RecipesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "recipes"
    verbose_name = _("app__recipes")


__all__ = []
