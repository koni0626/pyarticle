# Generated by Django 3.0.8 on 2020-08-16 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyarticle', '0006_auto_20200815_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='update_date',
            field=models.DateTimeField(null=True, verbose_name='更新日'),
        ),
    ]