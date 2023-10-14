# Generated by Django 4.2.5 on 2023-10-09 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_remove_recipe_author_recipe_chef'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='url',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='vote_count',
        ),
        migrations.AddField(
            model_name='recipe',
            name='uploaded_image',
            field=models.ImageField(blank=True, null=True, upload_to='images\recipe_images'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='difficult',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='nutrients',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='rattings',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]