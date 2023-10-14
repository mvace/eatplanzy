from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("recipe/add_recipe/", views.add_recipe, name="add_recipe"),
    path("recipe/<slug:slug>/", views.recipe, name="recipe"),
    path("category/<slug:category>/", views.category, name="category"),
    path("add_favorite/<slug:slug>/", views.add_favorite, name="add_favorite"),
    path("remove_favorite/<slug:slug>/", views.remove_favorite, name="remove_favorite"),
]
