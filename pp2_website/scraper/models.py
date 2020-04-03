from django.db import models


class Opinion(models.Model):
    opinion_id = models.PositiveIntegerField()
    author = models.CharField(max_length=100)
    recomendation = models.CharField(max_length=100)
    stars = models.FloatField()
    pros = models.CharField(max_length=100)
    cons = models.CharField(max_length=100)
    purchased = models.CharField(max_length=100)
    purchase_date = models.CharField(max_length=100)
    review_date = models.CharField(max_length=100)
    usefull = models.CharField(max_length=100)
    useless = models.CharField(max_length=100)
    content = models.TextField()


class Product(models.Model):
    # Ogólne informacje
    ceneo_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    img = models.CharField(max_length=150)
    min_img_1 = models.CharField(max_length=150)
    min_img_2 = models.CharField(max_length=150)
    min_img_3 = models.CharField(max_length=150)
    price = models.CharField(max_length=100)

    # Opinie
    average_rating = models.FloatField()
    opinions_number = models.PositiveIntegerField()
    pros_number = models.PositiveIntegerField()
    cons_number = models.PositiveIntegerField()

    # Liczba gwiazdek
    stars_full = models.PositiveIntegerField()
    stars_empty = models.PositiveIntegerField()
    star_1 = models.PositiveIntegerField()
    star_2 = models.PositiveIntegerField()
    star_3 = models.PositiveIntegerField()
    star_4 = models.PositiveIntegerField()
    star_5 = models.PositiveIntegerField()

    # Rekomendacje
    recomended = models.PositiveIntegerField()
    notrecomended = models.PositiveIntegerField()
    neutral = models.PositiveIntegerField()

    opinions = models.ManyToManyField(Opinion, blank=True)

    def __str__(self):
        return self.name
