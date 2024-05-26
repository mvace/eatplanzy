from rest_framework import serializers
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "name",
            "user",
            "profile_picture",
            "bio",
            "social_links",
            "user_recipes",
        ]
