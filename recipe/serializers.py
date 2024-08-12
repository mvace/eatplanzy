from rest_framework import serializers
from recipe.models import Recipe
from django.contrib.auth.models import User


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = [
            "name",
            "id",
            "chef",
            "image",
            "description",
            "ingredients",
            "steps",
            "nutrients",
            "times",
            "serves",
            "subcategory",
            "dish_type",
            "maincategory",
        ]
