# Generated by Django 4.2.5 on 2023-10-14 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default='static/images/default_user_image.png', upload_to='images/profile_pic'),
        ),
    ]
