from django.core.validators import MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mdeditor.fields import MDTextField
from sorl.thumbnail import get_thumbnail


from core.models import NormalizedNameMixin, UniqueNormalizedNameMixin
from core.utils import RandomFileName, render_markdown, Thumbnail
from recipes.managers import RecipeManager
from users.models import User


class RecipeLevel(models.IntegerChoices):
    EASY = 1, _("recipes__level_choices__easy")
    NORMAL = 2, _("recipes__level_choices__normal")
    HARD = 3, _("recipes__level_choices__hard")
    EXTREME = 4, _("recipes__level_choices__extreme")


class IngredientUnit(models.TextChoices):
    G = "G", _("recipes__unit_choices__grams")
    KG = "KG", _("recipes__unit_choices__kilogramme")
    L = "L", _("recipes__unit_choices__litre")
    ML = "ML", _("recipes__unit_choices__millilitre")
    PIECE = "PIECE", _("recipes__unit_choices__piece")
    PINCH = "PINCH", _("recipes__unit_choices__pinch")
    TEASPOON = "TEASPOON", _("recipes__unit_choices__tea_spoon")
    TABLESPOON = "TABLESPOON", _("recipes__unit_choices__table_spoon")
    CUP = "CUP", _("recipes__unit_choices__cup")


class RecipeState(models.TextChoices):
    PUBLISHED = "PUB", _("recipes__recipe_state__published")
    MODERATED = "MOD", _("recipes__recipe_state__moderated")
    REJECTED = "REJ", _("recipes__recipe_state__rejected")


class Category(UniqueNormalizedNameMixin, models.Model):
    name = models.CharField(
        verbose_name=_("recipes__model__category__name"),
        max_length=127,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("recipes__model__category__verbose_name")
        verbose_name_plural = _(
            "recipes__model__category__verbose_name_plural",
        )

    def __str__(self):
        return self.name


class Kitchen(UniqueNormalizedNameMixin, models.Model):
    name = models.CharField(
        verbose_name=_("recipes__model__kitchen__name"),
        max_length=127,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("recipes__model__kitchen__verbose_name")
        verbose_name_plural = _("recipes__model__kitchen__verbose_name_plural")

    def __str__(self):
        return self.name


class Ingredient(UniqueNormalizedNameMixin, models.Model):
    name = models.CharField(
        verbose_name=_("recipes__model__ingredient__name"),
        max_length=127,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = _("recipes__model__ingredient__verbose_name")
        verbose_name_plural = _(
            "recipes__model__ingredient__verbose_name_plural",
        )

    def __str__(self):
        return self.name


class Recipe(NormalizedNameMixin, models.Model):
    objects: RecipeManager = RecipeManager()

    name = models.CharField(
        verbose_name=_("recipes__model__recipe__name"),
        max_length=255,
    )
    author = models.ForeignKey(
        User,
        related_name="recipes",
        verbose_name=_("model__foreign__author"),
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
    state = models.CharField(
        max_length=3,
        verbose_name=_("recipes__model__recipe__state"),
        choices=RecipeState.choices,
        default=RecipeState.MODERATED,
    )
    categories = models.ManyToManyField(
        Category,
        related_name="recipes",
        verbose_name=_("model__foreign__categories"),
        blank=True,
    )
    kitchen = models.ForeignKey(
        Kitchen,
        related_name="recipes",
        verbose_name=_("model__foreign__kitchen"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    instruction = MDTextField(
        verbose_name=_("recipes__model__recipe__instruction"),
        max_length=8191,
    )
    main_image = models.ImageField(
        verbose_name=_("recipes__model__recipe__main_image"),
        upload_to=RandomFileName("recipes/main_image/"),
        blank=True,
        null=True,
    )
    level = models.IntegerField(
        choices=RecipeLevel.choices,
        verbose_name=_("recipes__model__recipe__level"),
    )
    time = models.PositiveIntegerField(
        verbose_name=_("recipes__model__recipe__time"),
    )

    class Meta:
        verbose_name = _("recipes__model__recipe__verbose_name")
        verbose_name_plural = _("recipes__model__recipe__verbose_name_plural")

    def __str__(self):
        if len(self.name) > 100:
            return self.name[:100] + "..."

        return self.name

    def get_rendered_instruction(self) -> str:
        return render_markdown(self.instruction)

    def get_image_500(self) -> Thumbnail | None:
        if not self.main_image:
            return None

        return get_thumbnail(self.main_image, "500", quality=85)

    def get_image_128x128(self) -> Thumbnail | None:
        if not self.main_image:
            return None

        return get_thumbnail(
            self.main_image,
            "128x128",
            crop="center",
            quality=51,
        )

    def image_tmb(self) -> str:
        if self.main_image:
            return mark_safe(
                f'<img src="{self.get_image_128x128().url}"',
            )

        return _("model__image__no_image")

    image_tmb.short_description = _("model__image__preview")
    image_tmb.allow_tags = True


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="ingredients",
        verbose_name=_("model__foreign__recipe"),
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name=_("model__foreign__ingredient"),
    )
    count = models.FloatField(
        verbose_name=_("recipes__model__recipe_ingredient__count"),
        validators=[
            MinValueValidator(0),
        ],
    )
    unit = models.CharField(
        max_length=12,
        verbose_name=_("recipes__model__recipe_ingredient__unit"),
        choices=IngredientUnit.choices,
    )

    class Meta:
        unique_together = ("recipe", "ingredient")
        verbose_name = _("recipes__model__recipe_ingredient__verbose_name")
        verbose_name_plural = _(
            "recipes__model__recipe_ingredient__verbose_name_plural",
        )

    def __str__(self):
        return _("recipes__model__recipe_ingredient__str") % {
            "id": self.id,
            "ingredient": self.ingredient_id,
            "recipe": self.recipe_id,
        }


class RecipeImage(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name=_("model__foreign__recipe"),
    )
    image = models.ImageField(
        upload_to=RandomFileName("recipes/recipe/"),
        verbose_name=_("recipes__model__recipe_image__image"),
    )

    class Meta:
        verbose_name = _("recipes__model__recipe_image__verbose_name")
        verbose_name_plural = _(
            "recipes__model__recipe_image__verbose_name_plural",
        )

    def __str__(self):
        return _("recipes__model__recipe_image__str") % {
            "id": self.id,
            "recipe": self.recipe_id,
        }

    def get_image_500(self) -> Thumbnail | None:
        if not self.image:
            return None

        return get_thumbnail(self.image, "500", quality=85)

    def get_image_128x128(self) -> Thumbnail | None:
        if not self.image:
            return None

        return get_thumbnail(self.image, "128x128", crop="center", quality=51)

    def image_tmb(self) -> str:
        if not self.image:
            return _("model__image__no_image")

        return mark_safe(
            f'<img src="{self.get_image_128x128().url}"',
        )

    image_tmb.short_description = _("model__image__preview")
    image_tmb.allow_tags = True


__all__ = []
