from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username}"

    def get_like_count(self):
        return CommentLike.objects.filter(comment=self).count()


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "comment"]


class Recipe(models.Model):
    def generate_slugified_filename(instance, filename):
        original_filename, file_extension = filename.split(".")
        slugified_filename = slugify(original_filename)
        return f"images/recipe_images/{slugified_filename}.{file_extension}"

    name = models.CharField(max_length=255, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chef = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    uploaded_image = models.ImageField(
        upload_to=generate_slugified_filename, null=True, blank=True
    )

    description = models.TextField()
    ingredients = models.JSONField()
    steps = models.JSONField()
    nutrients = models.JSONField(null=True, blank=True)
    times = models.JSONField(default=dict)
    serves = models.PositiveIntegerField()
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
