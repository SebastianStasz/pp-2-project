# Generated by Django 3.0.4 on 2020-03-31 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0007_opinion'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='opinions',
            field=models.ManyToManyField(blank=True, to='scraper.Opinion'),
        ),
    ]
