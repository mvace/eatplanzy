from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("recipe/<slug:slug>/", views.recipe, name="recipe"),
    path("category/<slug:category>/", views.category, name="category"),
]
