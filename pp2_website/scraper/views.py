import requests
from bs4 import BeautifulSoup
import pprint
import json

from django.shortcuts import render
from .models import Product
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from scraper.models import Product, Opinion
from django.core import serializers


class ProductListView(ListView):
    model = Product
    template_name = 'scraper/products.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


class ProductChartslView(DetailView):
    model = Product
    template_name = 'scraper/product-charts.html'


def productDownload(request):
    product_id = request.GET['product_id']
    product = Product.objects.get(pk=product_id)
    opinion_list = product.opinions.all()

    filedata = serializers.serialize('json', opinion_list)
    response = HttpResponse(filedata)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = f'attachment; filename=Oceneo - {product_id}.json'
    return response


def home(request):
    return render(request, 'scraper/index.html', {'title': 'Strona główna'})


def author(request):
    return render(request, 'scraper/author.html', {'title': 'Autor'})


def products(request):
    context = {
        'title': 'Produkty',
        'products': Product.objects.all()
    }
    return render(request, 'scraper/products.html', context)


def singleProduct(request):
    return render(request, 'scraper/single_product.html', {'title': 'Product'})


def extraction(request):
    message = ''
    if request.method == "POST":
        to_save = request.POST.get("save", None)
        product_id = request.POST.get('web_link', None)

        if product_id == '':
            return render(request, 'scraper/extraction.html', {'title': 'Ekstrakcja opinii', 'message': 'Pole jest puste'})

        opinions_list = []
        recomended = 0
        notrecomended = 0
        neutral = 0
        star_1 = 0
        star_2 = 0
        star_3 = 0
        star_4 = 0
        star_5 = 0

        url_prefix = "https://www.ceneo.pl"
        url_postfix = "#tab=reviews"
        url = url_prefix+"/"+str(product_id)+url_postfix

        page_respons = requests.get(url)
        page_tree = BeautifulSoup(page_respons.text, 'html.parser')
        opinions_ul = page_tree.find("ol", "js_product-reviews")

        if opinions_ul == None:
            return render(request, 'scraper/extraction.html', {'title': 'Ekstrakcja opinii', 'message': 'Nie znaleziono'})

        opinions = opinions_ul.find_all("li", "review-box")

        # wydobycie składowych dla produktu
        product_name = page_tree.find("h1", "product-name").string
        product_img = page_tree.find(
            "a", "js_image-preview").find("img")['src']
        product_price = page_tree.find(
            "span", "price").find("span", "value").string
        product_score = float(page_tree.find(
            "span", "product-score").text[:3].replace(',', '.'))
        product_category = page_tree.find("nav", "breadcrumbs").find_all("div")[
            2].find("span").string
        product_full_stars = int(round(product_score))
        product_empty_stars = 5 - product_full_stars
        product_pros_number = 0
        product_cons_number = 0

        product = {
            'product_name': product_name,
            'product_img': product_img,
            'product_price': product_price,
            'product_score': product_score,
            'product_category': product_category,
            'product_full_stars': product_full_stars,
            'product_empty_stars': product_empty_stars
        }

        # wydobycie składowych dla pojedynczej opinii
        while url:
            page_respons = requests.get(url)
            page_tree = BeautifulSoup(page_respons.text, 'html.parser')
            opinions_ul = page_tree.find("ol", "js_product-reviews")
            opinions = opinions_ul.find_all("li", "review-box")

            for opinion in opinions:
                opinion_id = opinion["data-entry-id"]
                author = opinion.find("div", "reviewer-name-line").string

                stars = opinion.find("span", "review-score-count").string
                index = stars.index('/')
                stars = stars[:index]
                stars_round = float(stars.replace(',', '.'))

                if stars_round == 1 or stars_round == 0.5:
                    star_1 += 1
                elif stars_round == 2 or stars_round == 1.5:
                    star_2 += 1
                elif stars_round == 3 or stars_round == 2.5:
                    star_3 += 1
                elif stars_round == 4 or stars_round == 3.5:
                    star_4 += 1
                elif stars_round == 5 or stars_round == 4.5:
                    star_5 += 1

                dates = opinion.find("span", "review-time").find_all("time")
                review_date = dates.pop(0)["datetime"]
                useful = opinion.find("button", "vote-yes").find("span").string
                useless = opinion.find("button", "vote-no").find("span").string
                content = opinion.find("p", "product-review-body").get_text()

                try:
                    purchased = opinion.find(
                        "div", "product-review-pz").find("em").string
                except AttributeError:
                    purchased = 'Brak'

                try:
                    recommendation = opinion.find(
                        "div", "product-review-summary").find("em").string
                except AttributeError:
                    recommendation = 'Brak'

                if recommendation == 'Polecam':
                    recomended += 1
                elif recommendation == 'Nie polecam':
                    notrecomended += 1
                elif recommendation == 'Brak':
                    neutral += 1

                try:
                    purchase_date = dates.pop(0)["datetime"]
                except IndexError:
                    purchase_date = 'Brak'

                try:
                    pros = opinion.find(
                        "div", "pros-cell").find("ul")
                    product_pros_number += len(pros.find_all("li"))
                    pros = opinion.find(
                        "div", "pros-cell").find("ul").get_text()
                except AttributeError:
                    pros = 'Nie podano'

                try:
                    cons = opinion.find(
                        "div", "cons-cell").find("ul")
                    product_cons_number += len(cons.find_all("li"))
                    cons = opinion.find(
                        "div", "cons-cell").find("ul").get_text()
                except AttributeError:
                    cons = 'Nie podano'

                opinion_dict = {
                    "opinion_id": opinion_id,
                    "author": author,
                    "recommendation": recommendation,
                    "stars": stars_round,
                    "pros": pros,
                    "cons": cons,
                    "purchased": purchased,
                    "purchase_date": purchase_date,
                    "review_date": review_date,
                    "useful": useful,
                    "useless": useless,
                    "content": content
                }

                opinions_list.append(opinion_dict)

            try:
                url = url_prefix + \
                    page_tree.find("a", "pagination__next")["href"]
            except TypeError:
                url = None

            filee = json.dumps(opinions_list)
            opinions_number = len(opinions_list)

        # Zapisanie do bazy danych
        if to_save:
            if Product.objects.filter(ceneo_id=product_id).exists():
                message = f'Ten produkt jest w bazie danych'
            else:
                # Produkt
                message = f'Produkt został zapisany w bazie danych'
                product_object = Product(ceneo_id=product_id,
                                         name=product_name,
                                         category=product_category,
                                         img=product_img,
                                         price=product_price,
                                         average_rating=product_score,
                                         opinions_number=opinions_number,
                                         pros_number=product_pros_number,
                                         cons_number=product_cons_number,
                                         stars_full=product_full_stars,
                                         stars_empty=product_empty_stars,
                                         recomended=recomended,
                                         notrecomended=notrecomended,
                                         neutral=neutral,
                                         star_1=star_1,
                                         star_2=star_2,
                                         star_3=star_3,
                                         star_4=star_4,
                                         star_5=star_5,)
                product_object.save()

                # Opinie
                for opinion in opinions_list:
                    opinion_object = Opinion(
                        opinion_id=opinion.get('opinion_id'),
                        author=opinion.get('author'),
                        recomendation=opinion.get('recommendation'),
                        stars=opinion.get('stars'),
                        pros=opinion.get('pros'),
                        cons=opinion.get('cons'),
                        purchased=opinion.get('purchased'),
                        purchase_date=opinion.get('purchase_date'),
                        review_date=opinion.get('review_date'),
                        usefull=opinion.get('useful'),
                        useless=opinion.get('useless'),)
                    opinion_object.save()
                    product_object.opinions.add(opinion_object)

        # Przekierowanie na stronę produktu
        return render(request, 'scraper/single_product.html', {'title': 'Product', 'message': message, 'opinions': opinions_list, 'product': product, 'file': filee, 'filename': product_id, 'rec': recomended, 'notrec': notrecomended, 'neutral': neutral, 'star_1': star_1, 'star_2': star_2, 'star_3': star_3, 'star_4': star_4, 'star_5': star_5, 'full': product_full_stars, 'empty': product_empty_stars})

    # Przekierowanie na stronę ekstrakcji (czysty formularz)
    return render(request, 'scraper/extraction.html', {'title': 'Ekstrakcja opinii'})


def download_file(request):
    filename = request.GET['filename']
    filedata = request.GET['filedata']

    response = HttpResponse(filedata)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


def show_charts(request):
    rec = request.GET['rec']
    notrec = request.GET['notrec']
    neutral = request.GET['neutral']

    star_1 = request.GET['star_1']
    star_2 = request.GET['star_2']
    star_3 = request.GET['star_3']
    star_4 = request.GET['star_4']
    star_5 = request.GET['star_5']

    return render(request, 'scraper/charts.html', {'title': 'Wykresy', 'rec': rec, 'notrec': notrec, 'neutral': neutral, 'star_1': star_1, 'star_2': star_2, 'star_3': star_3, 'star_4': star_4, 'star_5': star_5})
