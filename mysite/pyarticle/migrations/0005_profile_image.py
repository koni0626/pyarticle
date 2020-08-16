# Generated by Django 3.0.8 on 2020-07-26 09:14

from django.db import migrations, models
import pyarticle.models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarticle', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to=pyarticle.models.get_profile_image_path, verbose_name='プロフィール画像'),
        ),
    ]