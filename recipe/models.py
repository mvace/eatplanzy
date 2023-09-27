from django.db import models


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

    def __str__(self):
        return self.name
