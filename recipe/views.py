from django.shortcuts import render
from recipe.models import Recipe


# Create your views here.
def recipe(request, slug):
    recipe = Recipe.objects.get(name_slug=slug)
    return render(request, "recipe/recipe.html", {"recipe": recipe})
