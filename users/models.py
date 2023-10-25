from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from recipe.models import Recipe


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name="conversations")


class Message(models.Model):
    conversation = models.ForeignKey(
        "Conversation",
        related_name="+",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.content}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to="images/profile_pic", blank=True, null=True
    )  # check if this works, check the static file settings
    name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    social_links = models.TextField(blank=True)
    favorite_recipes = models.ManyToManyField(
        Recipe, related_name="favorite_recipes", blank=True
    )
    user_recipes = models.ManyToManyField(
        Recipe, related_name="user_recipes", blank=True
    )

    def __str__(self):
        return self.user.username


def create_profile(
    sender, instance, created, **kwargs
):  # the paramateres are provided by post_save.connect
    if created:
        user_profile = UserProfile(user=instance)
        user_profile.save()


post_save.connect(create_profile, sender=User)
