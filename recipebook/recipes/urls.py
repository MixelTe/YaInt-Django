from django.urls import path

from recipes import views

app_name = "recipes"

urlpatterns = [
    path(
        "",
        views.MainView.as_view(),
        name="main",
    ),
    path(
        "search/",
        views.SearchView.as_view(),
        name="search",
    ),
    path(
        "recipe/<int:pk>",
        views.RecipeView.as_view(),
        name="recipe",
    ),
    path(
        "recipe/<int:pk>/edit",
        views.RecipeEditView.as_view(),
        name="recipe-edit",
    ),
    path(
        "recipe/add",
        views.RecipeAddView.as_view(),
        name="recipe-add",
    ),
]


__all__ = []
