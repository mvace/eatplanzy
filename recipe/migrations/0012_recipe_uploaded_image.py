# Generated by Django 4.2.5 on 2023-10-14 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_remove_recipe_uploaded_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='uploaded_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/recipe_images'),
        ),
    ]
