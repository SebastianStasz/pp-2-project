# Generated by Django 3.0.4 on 2020-03-30 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ceneo_id',
            field=models.PositiveIntegerField(default=123),
            preserve_default=False,
        ),
    ]
