from django.contrib import admin

from feedback import models


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        models.Comment.author.field.name,
        models.Comment.recipe.field.name,
    ]


@admin.register(models.Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        models.Rate.value.field.name,
        models.Rate.author.field.name,
        models.Rate.recipe.field.name,
    ]


__all__ = []
