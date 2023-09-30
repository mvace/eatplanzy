from django.shortcuts import render
from recipe.models import Recipe
from django.http import Http404


# Create your views here.
def recipe(request, slug):
    recipe = Recipe.objects.get(name_slug=slug)
    return render(request, "recipe/recipe.html", {"recipe": recipe})


def category(request, category):
    recipes = None

    if Recipe.objects.filter(maincategory_slug=category):
        recipes = Recipe.objects.filter(maincategory_slug=category)
    elif Recipe.objects.filter(subcategory_slug=category):
        recipes = Recipe.objects.filter(subcategory_slug=category)
    elif Recipe.objects.filter(dish_type_slug=category):
        recipes = Recipe.objects.filter(dish_type_slug=category)
    else:
        raise Http404

    count = recipes.count()

    return render(request, "recipe/category.html", {"recipes": recipes, "count": count})
