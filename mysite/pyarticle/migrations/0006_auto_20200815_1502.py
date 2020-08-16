# Generated by Django 3.0.8 on 2020-08-15 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarticle', '0005_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='belong',
        ),
        migrations.AddField(
            model_name='profile',
            name='wallet',
            field=models.CharField(help_text='NEMの振込先', max_length=1024, null=True, verbose_name='NEMの振込先'),
        ),
    ]