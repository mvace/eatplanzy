from rest_framework import serializers
from recipe.models import Recipe


class RecipeListSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name="recipe:recipe-detail", lookup_field="name_slug"
    )

    class Meta:
        model = Recipe
        fields = [
            "url",
            "name",
        ]


class RecipeDetailSerializer(serializers.ModelSerializer):

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
