# Generated by Django 3.0.8 on 2020-08-26 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarticle', '0013_book_footer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='wallet',
        ),
        migrations.AddField(
            model_name='profile',
            name='nem_address',
            field=models.CharField(help_text='NEMの振込先アドレス', max_length=1024, null=True, verbose_name='NEMの振込先アドレス'),
        ),
        migrations.AddField(
            model_name='profile',
            name='nem_message',
            field=models.CharField(help_text='NEMメッセージ', max_length=1024, null=True, verbose_name='NEMメッセージ'),
        ),
    ]
