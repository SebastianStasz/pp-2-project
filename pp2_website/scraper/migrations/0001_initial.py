# Generated by Django 3.0.4 on 2020-03-27 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('img', models.CharField(max_length=150)),
                ('average_rating', models.FloatField()),
                ('opinions_number', models.PositiveIntegerField()),
                ('pros_number', models.PositiveIntegerField()),
                ('cons_number', models.PositiveIntegerField()),
            ],
        ),
    ]