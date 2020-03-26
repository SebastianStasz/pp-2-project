from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'scraper/index.html', {'title:': 'Strona główna'})


def author(request):
    return render(request, 'scraper/author.html', {'title:': 'Autor'})


def extraction(request):
    return render(request, 'scraper/extraction.html', {'title:': 'Ekstrakcja opinii'})


def products(request):
    return render(request, 'scraper/products.html', {'title:': 'Produkty'})
