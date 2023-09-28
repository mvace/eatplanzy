from django.shortcuts import render
from recipe.models import Recipe


# Create your views here.
def recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    return render(request, "recipe/recipe.html", {"recipe": recipe})
