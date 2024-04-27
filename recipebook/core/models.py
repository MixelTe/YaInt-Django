from typing import Any

from django.core import exceptions
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext as _

from core.utils import normalize_name


class NormalizedNameMixin(models.Model):
    name: models.CharField

    normalized_name = models.CharField(
        editable=False,
        max_length=127,
    )

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        normalized = normalize_name(self.name)
        self.normalized_name = normalized
        super().save(*args, **kwargs)


class UniqueNormalizedNameMixin(models.Model):
    name: models.CharField

    normalized_name = models.CharField(
        unique=True,
        editable=False,
        max_length=127,
    )

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        normalized = normalize_name(self.name)
        self.normalized_name = normalized
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        normalized = normalize_name(self.name)
        if self._state.adding:
            existing = self.__class__.objects.filter(
                normalized_name=normalized,
            ).exists()
        else:
            existing = (
                self.__class__.objects.exclude(pk=self.pk)
                .filter(normalized_name=normalized)
                .exists()
            )

        if existing:
            raise exceptions.ValidationError(
                {
                    self.__class__.name.field.name: _("error__no_unique_name"),
                },
            )


@receiver(models.signals.pre_save)
def pre_save(
    sender: str,
    instance: Any,
    raw: bool = False,
    **kwargs: Any,
) -> None:
    if not raw:
        return

    if not isinstance(
        instance,
        (NormalizedNameMixin, UniqueNormalizedNameMixin),
    ):
        return

    normalized = normalize_name(instance.name)
    instance.normalized_name = normalized


__all__ = []
