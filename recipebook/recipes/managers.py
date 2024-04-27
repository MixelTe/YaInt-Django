from functools import cached_property
from typing import TypedDict

from django.db.models import Manager, Prefetch
from django.db.models.query import QuerySet

from core.utils import normalize_name
from recipes import models
from users.models import User


class SearchParams(TypedDict, total=False):
    sn: str  # name
    sc: str  # category
    si: str  # ingredients
    sie: str  # exclude ingredients
    sk: str  # kitchen
    sl: str  # level
    order: str


class RecipeManager(Manager["models.Recipe"]):
    @cached_property
    def ordering(self) -> dict[str, list[str]]:
        field_name = models.Recipe.name.field.name
        return {
            "new": ["-" + models.Recipe.created.field.name, field_name],
            "easy": [models.Recipe.level.field.name, field_name],
            "fast": [models.Recipe.time.field.name, field_name],
            "name": [field_name],
        }

    def published(self) -> QuerySet:
        return self.get_queryset().filter(
            **{
                models.Recipe.state.field.name: models.RecipeState.PUBLISHED,
            },
        )

    def search(self, params: SearchParams) -> QuerySet:
        queryset = self.published()
        filter_fields = {}
        exclude_fields = {}

        name = params.get("sn", "")
        if name:
            name = normalize_name(name)
            field = models.Recipe.normalized_name.field.name + "__contains"
            filter_fields[field] = name

        category = params.get("sc", "")
        if category.isdigit():
            field = models.Recipe.categories.field.name + "__in"
            filter_fields[field] = [category]

        field_ings = models.Recipe.ingredients.field.related_query_name()
        field_ing = models.RecipeIngredient.ingredient.field.name
        field = field_ings + "__" + field_ing + "__in"
        ingredients = params.get("si", "")
        if ingredients:
            ingredients = [
                int(v) for v in ingredients.split("-") if v.isdigit()
            ]
            filter_fields[field] = ingredients

        ingredients_exclude = params.get("sie", "")
        if ingredients_exclude:
            ingredients = [
                int(v) for v in ingredients_exclude.split("-") if v.isdigit()
            ]
            exclude_fields[field] = ingredients

        kitchen = params.get("sk", "")
        if kitchen.isdigit():
            field = models.Recipe.kitchen.field.name
            filter_fields[field] = kitchen

        level = params.get("sl", "")
        if level.isdigit():
            field = models.Recipe.level.field.name
            filter_fields[field] = level

        if filter_fields:
            queryset = queryset.filter(**filter_fields)

        if exclude_fields:
            queryset = queryset.exclude(**exclude_fields)

        order_key = params.get("order", "name")
        order = self.ordering.get(order_key, self.ordering["name"])

        return queryset.order_by(*order)

    def optimize_for_search_page(self, queryset: QuerySet) -> QuerySet:
        queryset = queryset.select_related(
            models.Recipe.author.field.name,
            models.Recipe.kitchen.field.name,
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                models.Recipe.categories.field.name,
                queryset=models.Category.objects.all().only(
                    models.Category.name.field.name,
                ),
            ),
            Prefetch(
                models.Recipe.ingredients.field.related_query_name(),
                queryset=models.RecipeIngredient.objects.all()
                .select_related(models.RecipeIngredient.ingredient.field.name)
                .only(
                    models.RecipeIngredient.recipe.field.name,
                    models.RecipeIngredient.ingredient.field.name
                    + "__"
                    + models.Ingredient.name.field.name,
                    models.RecipeIngredient.count.field.name,
                    models.RecipeIngredient.unit.field.name,
                ),
            ),
        )
        return queryset.only(
            models.Recipe.name.field.name,
            models.Recipe.author.field.name + "__" + User.username.field.name,
            models.Recipe.created.field.name,
            models.Recipe.state.field.name,
            models.Recipe.kitchen.field.name
            + "__"
            + models.Kitchen.name.field.name,
            models.Recipe.main_image.field.name,
            models.Recipe.level.field.name,
            models.Recipe.time.field.name,
        )

    def optimize_for_detail_page(self, queryset: QuerySet) -> QuerySet:
        queryset = queryset.select_related(
            models.Recipe.author.field.name,
            models.Recipe.kitchen.field.name,
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                models.Recipe.categories.field.name,
                queryset=models.Category.objects.all().only(
                    models.Category.name.field.name,
                ),
            ),
            Prefetch(
                models.Recipe.ingredients.field.related_query_name(),
                queryset=models.RecipeIngredient.objects.all()
                .select_related(models.RecipeIngredient.ingredient.field.name)
                .only(
                    models.RecipeIngredient.recipe.field.name,
                    models.RecipeIngredient.ingredient.field.name
                    + "__"
                    + models.Ingredient.name.field.name,
                    models.RecipeIngredient.count.field.name,
                    models.RecipeIngredient.unit.field.name,
                ),
            ),
        )
        return queryset.only(
            models.Recipe.name.field.name,
            models.Recipe.author.field.name + "__" + User.username.field.name,
            models.Recipe.created.field.name,
            models.Recipe.state.field.name,
            models.Recipe.kitchen.field.name
            + "__"
            + models.Kitchen.name.field.name,
            models.Recipe.main_image.field.name,
            models.Recipe.level.field.name,
            models.Recipe.time.field.name,
            models.Recipe.instruction.field.name,
        )


__all__ = []
