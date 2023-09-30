from django.core.management.base import BaseCommand
from recipe.models import Recipe
from django.db.models import Count


class Command(BaseCommand):
    help = "Remove duplicate records from Recipe model based on name_slug"

    def handle(self, *args, **kwargs):
        duplicate_name_slugs = (
            Recipe.objects.values("name_slug")
            .annotate(count=Count("name_slug"))
            .filter(count__gt=1)
        )

        for name_slug_info in duplicate_name_slugs:
            name_slug = name_slug_info["name_slug"]
            count = name_slug_info["count"]
            self.stdout.write(f"Duplicate name_slug: {name_slug}, Count: {count}")

            # Retrieve all duplicates for the current name_slug
            duplicates_to_delete = Recipe.objects.filter(name_slug=name_slug)

            # Keep the first record and delete the rest
            keep_record = duplicates_to_delete.first()
            duplicates_to_delete.exclude(pk=keep_record.pk).delete()
            print("Duplicates deleted")

        self.stdout.write(
            self.style.SUCCESS("Duplicates based on name_slug removed successfully")
        )
