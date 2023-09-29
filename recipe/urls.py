from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("recipe/<slug:slug>/", views.recipe, name="recipe"),
]
