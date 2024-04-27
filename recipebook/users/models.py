from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from sorl.thumbnail import get_thumbnail

from core.utils import RandomFileName, Thumbnail


class UserManager(BaseUserManager):
    @classmethod
    def normalize_email(cls, email: str | None) -> str:
        email = super().normalize_email(email)
        if "@" not in email:
            return email

        email = email.lower()
        username, domain = email.split("@")

        if domain == "ya.ru":
            domain = "yandex.ru"

        if "+" in username:
            username = username.split("+")[0]

        if domain == "gmail.com":
            username = username.replace(".", "")

        if domain == "yandex.ru":
            username = username.replace(".", "-")

        return f"{username}@{domain}"

    def active(self) -> models.query.QuerySet:
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail: str) -> "User | None":
        mail = self.normalize_email(mail)
        try:
            return self.get_queryset().get(email=mail)
        except User.DoesNotExist:
            return None

    def by_username(self, username: str) -> "User | None":
        try:
            return self.get_queryset().get(username=username)
        except User.DoesNotExist:
            return None


class User(AbstractUser):
    objects: UserManager["User"] = UserManager()

    email = models.EmailField(
        verbose_name=_("users__model__user__email"),
        unique=True,
    )
    image = models.ImageField(
        verbose_name=_("users__model__user__image"),
        upload_to=RandomFileName("users/image/"),
        null=True,
        blank=True,
    )
    trusted = models.BooleanField(
        verbose_name=_("users__model__user__trusted"),
        default=False,
    )
    attempts_count = models.PositiveIntegerField(
        verbose_name=_("users__model__user__attempts_count"),
        default=0,
    )
    deactivation_date = models.DateTimeField(
        verbose_name=_("users__model__user__deactivation_date"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("users__model__user__verbose_name")
        verbose_name_plural = _(
            "users__model__user__verbose_name_plural",
        )

    def get_image_32x32(self) -> Thumbnail | None:
        if not self.image:
            return None

        return get_thumbnail(
            self.image,
            "32x32",
            crop="center",
            quality=85,
            format="PNG",
        )

    def get_image_128x128(self) -> Thumbnail | None:
        if not self.image:
            return None

        return get_thumbnail(
            self.image,
            "128x128",
            crop="center",
            quality=85,
            format="PNG",
        )

    def image_tmb(self) -> str:
        if self.image:
            return mark_safe(
                f'<img src="{self.get_image_128x128().url}"',
            )

        return _("model__image__no_image")

    image_tmb.short_description = _("model__image__preview")
    image_tmb.allow_tags = True


__all__ = []
