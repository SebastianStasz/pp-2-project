from django.db import models


class Product(models.Model):
    ceneo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    img = models.CharField(max_length=150)
    average_rating = models.FloatField()
    opinions_number = models.PositiveIntegerField()
    pros_number = models.PositiveIntegerField()
    cons_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name
