from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Recipe(models.Model):
    id = models.UUIDField(primary_key=True)
    url = models.URLField()
    image = models.URLField()
    name = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    rattings = models.PositiveIntegerField()
    ingredients = models.JSONField()
    steps = models.JSONField()
    nutrients = models.JSONField()
    times = models.JSONField()
    serves = models.PositiveIntegerField()
    difficult = models.CharField(max_length=255)
    vote_count = models.PositiveIntegerField()
    subcategory = models.CharField(max_length=255)
    dish_type = models.CharField(max_length=255)
    maincategory = models.CharField(max_length=255)
    maincategory_slug = models.SlugField(max_length=100, blank=True)
    subcategory_slug = models.SlugField(max_length=100, blank=True)
    name_slug = models.SlugField(max_length=255, blank=True)
    dish_type_slug = models.SlugField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically generate slugs when saving the object
        self.maincategory_slug = slugify(self.maincategory)
        self.subcategory_slug = slugify(self.subcategory)
        self.name_slug = slugify(self.name)
        self.dish_type_slug = slugify(self.dish_type)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.name}"
