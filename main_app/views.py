from django.shortcuts import render
from recipe.models import Recipe
from django.db.models import F, Func, Value
import random


# Create your views here.
def index(request):
    # Get all the IDs from the Recipe model
    recipe_ids = list(
        Recipe.objects.exclude(maincategory__in=["inspiration", "baking"]).values_list(
            "id", flat=True
        )
    )

    # Get 5 random IDs
    random_recipe_ids = random.sample(recipe_ids, 120)

    # Fetch the Recipe objects with the selected random IDs
    random_recipes = Recipe.objects.filter(id__in=random_recipe_ids)

    return render(request, "main_app/index.html", {"recipes": random_recipes})
