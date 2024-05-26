from rest_framework import serializers
from recipe.models import Recipe
from django.contrib.auth.models import User

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["id", "name", "description", "ingredients", "steps", "nutrients"]


