# Generated by Django 3.0.8 on 2020-11-28 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarticle', '0014_auto_20200826_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='draft',
            field=models.IntegerField(default=0, help_text='下書き', verbose_name='下書き'),
        ),
    ]