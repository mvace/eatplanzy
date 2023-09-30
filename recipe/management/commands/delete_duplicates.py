from django.core.management.base import BaseCommand
from recipe.models import Recipe
from django.db.models import Count


class Command(BaseCommand):
    help = "Remove duplicate records from Recipe model"

    def handle(self, *args, **kwargs):
        duplicate_urls = (
            Recipe.objects.values("url")
            .annotate(count=Count("url"))
            .filter(count__gt=1)
        )

        for url_info in duplicate_urls:
            url = url_info["url"]
            count = url_info["count"]
            self.stdout.write(f"Duplicate URL: {url}, Count: {count}")

            # Retrieve all duplicates for the current URL
            duplicates_to_delete = Recipe.objects.filter(url=url)

            # Keep the first record and delete the rest
            keep_record = duplicates_to_delete.first()
            duplicates_to_delete.exclude(pk=keep_record.pk).delete()
            print("Duplicate deleted")

        self.stdout.write(self.style.SUCCESS("Duplicates removed successfully"))
