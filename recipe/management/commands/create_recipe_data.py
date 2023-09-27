import json
from django.core.management.base import BaseCommand
from recipe.models import Recipe


class Command(BaseCommand):
    help = "Populate the database with recipe data from a JSON file"

    def handle(self, *args, **options):
        file_path = r"C:\Users\marek\dev\EatPlanzy\DataSet\BBC recipes\inspiration.json"  # Replace with the actual JSON file path

        with open(file_path, "r") as json_file:
            recipes_data = json.load(json_file)

        for recipe_data in recipes_data:
            recipe = Recipe(
                id=recipe_data["id"],
                url=recipe_data["url"],
                image=recipe_data["image"],
                name=recipe_data["name"],
                description=recipe_data["description"],
                author=recipe_data["author"],
                rattings=recipe_data["rattings"],
                ingredients=recipe_data["ingredients"],
                steps=recipe_data["steps"],
                nutrients=recipe_data["nutrients"],
                times=recipe_data["times"],
                serves=recipe_data["serves"],
                difficult=recipe_data["difficult"],
                vote_count=recipe_data["vote_count"],
                subcategory=recipe_data["subcategory"],
                dish_type=recipe_data["dish_type"],
                maincategory=recipe_data["maincategory"],
            )
            recipe.save()
            self.stdout.write(
                self.style.SUCCESS(f"Successfully imported recipe: {recipe.name}")
            )
