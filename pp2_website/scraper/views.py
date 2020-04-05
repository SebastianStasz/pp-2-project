from bs4 import BeautifulSoup
import requests
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from django.views.generic import ListView, DetailView
from scraper.models import Product, Opinion
from .models import Product


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


def extraction(request):
    message = ''
    if request.method == "POST":
        to_save = request.POST.get("save", None)
        product_id = request.POST.get('web_link', None)

        # Pusty formularz
        if product_id == '':
            context = {
                'title': 'Ekstrakcja opinii',
                'message': 'Pole jest puste'
                }
            return render(request, 'scraper/extraction.html', context)

        url_prefix = "https://www.ceneo.pl"
        url_postfix = "#tab=reviews"
        url = url_prefix+"/"+str(product_id)+url_postfix

        page_respons = requests.get(url)
        page_tree = BeautifulSoup(page_respons.text, 'html.parser')
        opinions_ul = page_tree.find("ol", "js_product-reviews")

        # Nie znaleziono produktu
        if opinions_ul == None:
            context = {
                'title': 'Ekstrakcja opinii',
                'message': 'Nie znaleziono'
                }
            return render(request, 'scraper/extraction.html', context)

        opinions = opinions_ul.find_all("li", "review-box")

        # Definicja zmiennych
        product_min_img_list = []
        opinions_list = []
        product_pros_number = product_cons_number = 0
        recomended = notrecomended = neutral = 0
        star_1 = star_2 = star_3 = star_4 = star_5 = 0

        # wydobycie składowych dla produktu
        product_name = page_tree.find("h1", "product-name").text
        product_price = page_tree.find("span", "price").find("span", "value").string
        product_score = float(page_tree.find("span", "product-score").text[:3].replace(',', '.'))
        product_category = page_tree.find("nav", "breadcrumbs").find_all("div")[2].find("span").string
        product_full_stars = round(product_score)
        product_empty_stars = 5 - product_full_stars

        try:
            product_img = page_tree.find("a", "js_image-preview").find("img")['src']
            try:
                product_img_list = page_tree.find("ul", "js_product-pictures-miniatures").find_all("li")
                product_img_list.pop(0)
                for el in product_img_list:
                    if el['class'] == ['js_product-image-miniature_el', 'hidden']: product_min_img_list.append(None)
                    else:
                        el = el.find("a")
                        product_min_img_list.append(el['href'])
                    if len(product_min_img_list) == 3: break # Na potrzeby projektu, pobierz tylko 3 zdjęcia
                # Gdy zdjęć jest mniej niż trzy
                if len(product_min_img_list) == 1:
                    product_min_img_list.append(None)
                    product_min_img_list.append(None)
                elif len(product_min_img_list) == 2: product_min_img_list.append(None)
            except: product_img_list = [None, None , None]
        except:
            product_img = '//image.ceneostatic.pl/data/products/123123/f-tonsil-soundfinder-250.jpg'

        product = {
            'product_name': product_name,
            'product_img': product_img,
            'product_min_img': product_min_img_list,
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
                dates = opinion.find("span", "review-time").find_all("time")
                review_date = dates.pop(0)["datetime"]
                useful = opinion.find("button", "vote-yes").find("span").string
                useless = opinion.find("button", "vote-no").find("span").string
                content = opinion.find("p", "product-review-body").get_text()

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

                try: purchased = opinion.find("div", "product-review-pz").find("em").string
                except AttributeError: purchased = 'Brak'

                try: recommendation = opinion.find("div", "product-review-summary").find("em").string
                except AttributeError: recommendation = 'Brak'

                if recommendation == 'Polecam': recomended += 1
                elif recommendation == 'Nie polecam': notrecomended += 1
                elif recommendation == 'Brak': neutral += 1

                try: purchase_date = dates.pop(0)["datetime"]
                except IndexError: purchase_date = 'Brak'

                try:
                    pros = ''
                    pros_ul = opinion.find("div", "pros-cell").find("ul").find_all("li")
                    product_pros_number += len(pros_ul)
                    for el in pros_ul:
                        pros += el.text + ', '
                except AttributeError: pros = 'Nie podano'

                try:
                    cons = ''
                    cons_ul = opinion.find("div", "cons-cell").find("ul").find_all("li")
                    product_cons_number += len(cons_ul)
                    for el in cons_ul:
                        cons += el.text + ', '
                except AttributeError: cons = 'Nie podano'

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
                url = url_prefix + page_tree.find("a", "pagination__next")["href"]
            except TypeError:
                url = None

            filee = json.dumps(opinions_list)
            opinions_number = len(opinions_list)

        # Zapisanie do bazy danych
        if to_save:
            if Product.objects.filter(ceneo_id=product_id).exists():
                message = f'Ten produkt jest w bazie danych'
            else:
                message = f'Produkt został zapisany w bazie danych'

                # Produkt
                product_object = Product(
                    ceneo_id=product_id,
                    name=product_name,
                    category=product_category,
                    img=product_img,
                    min_img_1=product_min_img_list[0],
                    min_img_2=product_min_img_list[1],
                    min_img_3=product_min_img_list[2],
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
                        useless=opinion.get('useless'),
                        content=opinion.get('content'))
                    opinion_object.save()
                    product_object.opinions.add(opinion_object)

        # Przekierowanie na stronę produktu (dane z ekstrakcji)
        context = {
            'title': 'Product',
            'message': message,
            'opinions': opinions_list,
            'product': product,
            'file': filee,
            'filename': product_id,
            'rec': recomended,
            'notrec': notrecomended,
            'neutral': neutral,
            'star_1': star_1,
            'star_2': star_2,
            'star_3': star_3,
            'star_4': star_4,
            'star_5': star_5,
            'full': product_full_stars,
            'empty': product_empty_stars
        }
        return render(request, 'scraper/single_product.html', context)

    # Przekierowanie na stronę ekstrakcji (czysty formularz)
    return render(request, 'scraper/extraction.html', {'title': 'Ekstrakcja opinii'})


# Dla szablonów pobierających dane bezpośredni po ekstrakcji
def singleProduct(request):
    return render(request, 'scraper/single_product.html', {'title': 'Product'})


def download_file(request):
    filename = request.GET['filename']
    filedata = request.GET['filedata']

    response = HttpResponse(filedata)
    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = f'attachment; filename={filename}.json'
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

    context = {
        'title': 'Wykresy',
        'rec': rec,
        'notrec': notrec,
        'neutral': neutral,
        'star_1': star_1,
        'star_2': star_2,
        'star_3': star_3,
        'star_4': star_4,
        'star_5': star_5
    }

    return render(request, 'scraper/charts.html', context)


# Dla szablonów pobierających dane z bazy danych
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
