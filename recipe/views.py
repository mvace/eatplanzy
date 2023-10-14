from django.shortcuts import render, get_object_or_404, redirect
from recipe.models import Recipe
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.contrib import messages
from .forms import CommentForm, AddRecipeForm
from .models import Comment


# Create your views here.


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, name_slug=slug)
    if request.user.is_authenticated:
        form = CommentForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.recipe = recipe
                comment.save()
                messages.success(request, ("Your Comment Has Been Posted"))
                redirect(request.META.get("HTTP_REFERER"))

        comments = Comment.objects.filter(recipe=recipe)
        print(comments)
        return render(
            request,
            "recipe/recipe.html",
            {"recipe": recipe, "form": form, "comments": comments},
        )
    else:
        comments = Comment.objects.filter(recipe=recipe)
        return render(
            request, "recipe/recipe.html", {"recipe": recipe, "comments": comments}
        )


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


def add_favorite(request, slug):
    if request.user.is_authenticated:
        recipe = Recipe.objects.get(name_slug=slug)
        request.user.userprofile.favorite_recipes.add(recipe)
        request.user.userprofile.save()

        messages.success(request, ("Recipe added to your favourite recipes."))
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You have to be logged in."))
        return redirect(request.META.get("HTTP_REFERER"))


def remove_favorite(request, slug):
    recipe = Recipe.objects.get(name_slug=slug)
    request.user.userprofile.favorite_recipes.remove(recipe)
    request.user.userprofile.save()
    messages.success(request, ("Recipe removed from your favourite recipes."))
    return redirect(request.META.get("HTTP_REFERER"))


@login_required
def add_recipe(request):
    form = AddRecipeForm(request.POST or request.FILES)
    if request.method == "POST":
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.ingredients = form.cleaned_data["ingredients"].split("\n")
            recipe.steps = form.cleaned_data["steps"].split("\n")
            recipe.nutrients = form.cleaned_data["nutrients"].split("\n")
            recipe.user = request.user
            recipe.times = {}
            if "uploaded_image" in request.FILES:
                recipe.uploaded_image = request.FILES["uploaded_image"]
                current_site = get_current_site(request)
                img_url = f"http://{current_site}/media/images/recipe_images/{recipe.uploaded_image}"
                recipe.image = img_url

            recipe.save()

            messages.success(request, ("Your Recipe Has Been Added"))
            return redirect("main_app:index")
        else:
            print(form.errors)
    else:
        return render(request, "recipe/add_recipe.html", {"form": form})

    # else:
    #     messages.success(request, ("You Must Be Logged In To View That Page..."))
    #     return redirect("users:login_user")
