from django.test import TestCase
from django.contrib.auth.models import User
from recipe.models import Recipe
from django.utils.text import slugify
import uuid


class TestRecipeModel(TestCase):

    def setUp(self):
        # Set up a user for the ForeignKey relationship
        self.user = User.objects.create(username="testchef", password="password")
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            chef=self.user,
            description="A test recipe",
            ingredients={"ingredient1": "2 cups", "ingredient2": "1 tsp"},
            steps=["step 1", "step 2"],
            serves=4,
            subcategory="Desserts",
            dish_type="Cake",
            maincategory="Sweets",
        )

    def test_field_validation(self):
        # Test that name is unique
        with self.assertRaises(Exception):
            Recipe.objects.create(
                name="Test Recipe",
                description="Another test recipe",
                ingredients={"ingredient1": "2 cups", "ingredient2": "1 tsp"},
                steps=["step 1", "step 2"],
                serves=4,
                subcategory="Desserts",
                dish_type="Cake",
                maincategory="Sweets",
            )

    def test_slug_generation_on_save(self):
        # Test that the save method correctly slugifies fields
        self.recipe.save()
        self.assertEqual(
            self.recipe.maincategory_slug, slugify(self.recipe.maincategory)
        )
        self.assertEqual(self.recipe.subcategory_slug, slugify(self.recipe.subcategory))
        self.assertEqual(self.recipe.name_slug, slugify(self.recipe.name))
        self.assertEqual(self.recipe.dish_type_slug, slugify(self.recipe.dish_type))

    def test_generate_slugified_filename(self):
        # Test the generate_slugified_filename method
        filename = "Test Recipe Image.jpg"
        expected_filename = "images/recipe_images/test-recipe-image.jpg"
        generated_filename = Recipe.generate_slugified_filename(None, filename)
        self.assertEqual(generated_filename, expected_filename)

    def test_string_representation(self):
        # Test the __str__ method
        self.assertEqual(str(self.recipe), self.recipe.name)

    def test_chef_relationship(self):
        # Test that the ForeignKey relationship works as expected
        self.assertEqual(self.recipe.chef, self.user)

    def test_null_fields(self):
        # Test that nullable fields can be null
        recipe_with_null_fields = Recipe.objects.create(
            name="Null Field Recipe",
            description="A test recipe with null fields",
            ingredients={"ingredient1": "2 cups"},
            steps=["step 1"],
            serves=2,
            subcategory="Snacks",
            dish_type="Quick Bite",
            maincategory="Appetizers",
        )
        self.assertIsNone(recipe_with_null_fields.chef)
        self.assertIsNone(recipe_with_null_fields.image)
        self.assertIsNone(recipe_with_null_fields.nutrients)

    def test_default_values(self):
        # Test that default values are correctly set
        self.assertEqual(self.recipe.times, {})

    def test_uuid_field(self):
        # Test that the UUID field is automatically generated
        self.assertIsInstance(self.recipe.id, uuid.UUID)
