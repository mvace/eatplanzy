from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from recipe.models import Recipe, Comment, CommentLike
from django.urls import reverse
from django.http import Http404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from django.contrib import messages
from .forms import CommentForm, AddRecipeForm
from .models import Comment
from django.utils.text import slugify
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from recipe.serializers import RecipeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class RecipeList(APIView):
    """
    List all recipes, or create a new recipe.
    """

    def get(self, request, format=None):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, slug):
        try:
            return Recipe.objects.get(name_slug=slug)
        except Recipe.DoesNotExist:
            raise Http404

    def get(self, request, slug, format=None):
        recipe = self.get_object(slug)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def put(self, request, slug, format=None):
        recipe = self.get_object(slug)
        serializer = RecipeSerializer(recipe, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug, format=None):
        recipe = self.get_object(slug)
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def search(request):
    if request.method == "POST":
        search = f" {request.POST['search']} "
        print(type(search))
        results = Recipe.objects.filter(
            Q(ingredients__icontains=search)
            | Q(steps__icontains=search)
            | Q(name__icontains=search)
            | Q(description__icontains=search)
            | Q(subcategory__icontains=search)
            | Q(maincategory__icontains=search)
            | Q(dish_type__icontains=search)
        )
        print(results)

        return render(
            request, "recipe/search.html", {"results": results, "search": search}
        )
    else:
        return render(request, "recipe/search.html", {})


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


def comment_like(request, pk):
    if request.user.is_authenticated:
        user = request.user
        comment = get_object_or_404(Comment, id=pk)

        if CommentLike.objects.filter(user=user, comment=comment).exists():
            like = CommentLike.objects.get(user=user, comment=comment)
            like.delete()
        else:
            like = CommentLike(user=user, comment=comment)
            like.save()

        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You have to be logged in."))
        return redirect(request.META.get("HTTP_REFERER"))


def remove_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    comment.delete()
    messages.success(request, ("Your Comment Has Been Deleted"))
    return redirect(request.META.get("HTTP_REFERER"))


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
    if request.method == "POST":
        form = AddRecipeForm(request.POST or request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.ingredients = form.cleaned_data["ingredients"].split("\n")
            recipe.steps = form.cleaned_data["steps"].split("\n")
            recipe.nutrients = form.cleaned_data["nutrients"].split("\n")
            recipe.chef = request.user
            recipe.times = {}
            if "uploaded_image" in request.FILES:
                uploaded_image = request.FILES["uploaded_image"]
                recipe.uploaded_image = uploaded_image
                recipe.save()
                current_site = get_current_site(request)
                img_url = f"http://{current_site}/media/{recipe.uploaded_image}"
                recipe.image = img_url
            recipe.save()

            messages.success(request, ("Your Recipe Has Been Added"))
            return redirect("main_app:index")
        else:
            print(form.errors)
    else:
        form = AddRecipeForm()
        return render(request, "recipe/add_recipe.html", {"form": form})


@login_required
def update_recipe(request, slug):
    recipe = Recipe.objects.get(name_slug=slug)
    if recipe.chef_id == request.user.id:
        if request.method == "POST":
            form = AddRecipeForm(request.POST or request.FILES, instance=recipe)
            if form.is_valid():
                recipe = form.save(commit=False)
                recipe.ingredients = form.cleaned_data["ingredients"].split("\n")
                recipe.steps = form.cleaned_data["steps"].split("\n")
                recipe.nutrients = form.cleaned_data["nutrients"].split("\n")
                recipe.chef = request.user

                if "uploaded_image" in request.FILES:
                    recipe.uploaded_image = request.FILES["uploaded_image"]
                    current_site = get_current_site(request)
                    img_url = f"http://{current_site}/media/images/recipe_images/{recipe.uploaded_image}"
                    recipe.image = img_url
                else:
                    recipe.image = None

                recipe.save()

                messages.success(request, "Recipe updated successfully")
                return redirect(
                    reverse("recipe:recipe", kwargs={"slug": recipe.name_slug})
                )

        else:
            form = AddRecipeForm(instance=recipe)

        return render(request, "recipe/update_recipe.html", {"form": form})
    else:
        messages.success(request, "You do not have a permission to edit this recipe")
        return redirect("main_app:index")


def delete_recipe(request, slug):
    recipe = Recipe.objects.get(name_slug=slug)
    recipe.delete()
    messages.success(request, ("You've deleted the recipe."))
    return redirect("main_app:index")
