# Generated by Django 3.0.4 on 2020-03-30 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_product_ceneo_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ceneo_id',
            field=models.CharField(max_length=100),
        ),
    ]