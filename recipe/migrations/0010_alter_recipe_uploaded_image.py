# Generated by Django 4.2.5 on 2023-10-14 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_alter_recipe_id_alter_recipe_times_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='uploaded_image',
            field=models.ImageField(default='images/default_recipe_image.gif', upload_to='images/recipe_images'),
        ),
    ]
