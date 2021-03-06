# Generated by Django 3.0.4 on 2020-03-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0003_auto_20200330_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stars_empty',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='stars_full',
            field=models.PositiveIntegerField(default=3),
            preserve_default=False,
        ),
    ]
