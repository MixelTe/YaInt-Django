from django.db import models
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField

from core.utils import render_markdown
from recipes.models import Recipe
from users.models import User


class RatingChoices(models.IntegerChoices):
    HATE = 1, _("rating__rating_choices__hate")
    DISLIKE = 2, _("rating__rating_choices__dislike")
    NEUTRAL = 3, _("rating__rating_choices__neutral")
    LIKE = 4, _("rating__rating_choices__like")
    LOVE = 5, _("rating__rating_choices__love")


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        related_name="comments",
        verbose_name=_("model__foreign__author"),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="comments",
        verbose_name=_("model__foreign__recipe"),
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name=_("model__created"),
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name=_("model__updated"),
        auto_now=True,
    )
    text = MDTextField(
        max_length=2047,
        verbose_name=_("feedback__model__comment__text"),
    )

    class Meta:
        verbose_name = _("feedback__model__comment__verbose_name")
        verbose_name_plural = _(
            "feedback__model__comment__verbose_name_plural",
        )

    def __str__(self):
        return _("feedback__model__comment__str") % {
            "id": self.id,
            "author": self.author_id,
            "recipe": self.recipe_id,
        }

    def get_rendered_text(self) -> str:
        return render_markdown(self.text)


class Rate(models.Model):
    author = models.ForeignKey(
        User,
        related_name="ratings",
        verbose_name=_("model__foreign__author"),
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="ratings",
        verbose_name=_("model__foreign__recipe"),
        on_delete=models.CASCADE,
    )
    value = models.IntegerField(
        verbose_name=_("feedback__model__rate__value"),
        choices=RatingChoices.choices,
    )

    class Meta:
        verbose_name = _("feedback__model__rate__verbose_name")
        verbose_name_plural = _("feedback__model__rate__verbose_name_plural")

    def __str__(self):
        return _("feedback__model__rated__str") % {
            "id": self.id,
            "author": self.author_id,
            "recipe": self.recipe_id,
        }


class Cooked(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cooked",
        verbose_name=_("model__foreign__author"),
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="cooked",
        verbose_name=_("model__foreign__recipe"),
    )

    class Meta:
        unique_together = ("author", "recipe")
        verbose_name = _("feedback__model__cooked__verbose_name")
        verbose_name_plural = _("feedback__model__cooked__verbose_name_plural")

    def __str__(self):
        return _("feedback__model__cooked__str") % {
            "id": self.id,
            "author": self.author_id,
            "recipe": self.recipe_id,
        }


__all__ = []
