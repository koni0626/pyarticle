# Generated by Django 3.0.8 on 2020-12-20 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarticle', '0015_book_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='article_type',
            field=models.IntegerField(default=0, help_text='本の形式か日記の形式が選択できます', verbose_name='本の形式'),
        ),
    ]