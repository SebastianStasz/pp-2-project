# Generated by Django 3.0.4 on 2020-03-31 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0004_auto_20200330_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='neutral',
            field=models.PositiveIntegerField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='notrecomended',
            field=models.PositiveIntegerField(default=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='recomended',
            field=models.PositiveIntegerField(default=12),
            preserve_default=False,
        ),
    ]
