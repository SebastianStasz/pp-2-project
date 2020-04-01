# Generated by Django 3.0.4 on 2020-03-31 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0006_auto_20200331_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=100)),
                ('recomendation', models.CharField(max_length=100)),
                ('stars', models.FloatField()),
                ('pros', models.CharField(max_length=100)),
                ('cons', models.CharField(max_length=100)),
            ],
        ),
    ]