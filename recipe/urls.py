from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("recipe/add_recipe/", views.add_recipe, name="add_recipe"),
    path("recipe/<slug:slug>/", views.recipe, name="recipe"),
    path("recipe/delete/<slug:slug>/", views.delete_recipe, name="delete_recipe"),
    path("recipe/update/<slug:slug>/", views.update_recipe, name="update_recipe"),
    path("category/<slug:category>/", views.category, name="category"),
    path("add_favorite/<slug:slug>/", views.add_favorite, name="add_favorite"),
    path("remove_favorite/<slug:slug>/", views.remove_favorite, name="remove_favorite"),
    path("remove_comment/<int:pk>/", views.remove_comment, name="remove_comment"),
    path("comment/like/<int:pk>/", views.comment_like, name="comment_like"),
    path("search/", views.search, name="search"),
]
