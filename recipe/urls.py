from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("recipe/<str:pk>/", views.recipe, name="recipe"),
]
