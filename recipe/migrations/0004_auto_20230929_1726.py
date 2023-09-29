# Generated by Django 3.2.5 on 2023-09-29 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20230929_1721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='url_slug',
        ),
        migrations.AddField(
            model_name='recipe',
            name='name_slug',
            field=models.SlugField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='dish_type_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='maincategory_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='subcategory_slug',
            field=models.SlugField(blank=True, max_length=100),
        ),
    ]
