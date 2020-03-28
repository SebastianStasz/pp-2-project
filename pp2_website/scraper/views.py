import requests
from bs4 import BeautifulSoup
import pprint
import json

from django.shortcuts import render
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


def singleProduct(request):
    return render(request, 'scraper/single_product.html', {'title': 'Product'})


def extraction(request):
    if request.method == "POST":
        product_id = request.POST.get('web_link', None)

        if product_id == '':
            return render(request, 'scraper/extraction.html', {'title': 'Ekstrakcja opinii', 'message': 'Pole jest puste'})

        opinions_list = []
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
        product_score = page_tree.find("span", "product-score").text[:3]
        product_category = page_tree.find("nav", "breadcrumbs").find_all("div")[
            2].find("span").string
        product_full_stars = int(round(float(product_score.replace(',', '.'))))

        product = {
            'product_name': product_name,
            'product_img': product_img,
            'product_price': product_price,
            'product_score': product_score,
            'product_category': product_category,
            'product_full_stars': range(product_full_stars),
            'product_empty_stars': range(5 - product_full_stars)
        }
        print(opinions)

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
                dates = opinion.find("span", "review-time").find_all("time")
                review_date = dates.pop(0)["datetime"]
                useful = opinion.find("button", "vote-yes").find("span").string
                useless = opinion.find("button", "vote-no").find("span").string
                content = opinion.find("p", "product-review-body").get_text()

                try:
                    purchased = opinion.find(
                        "div", "product-review-pz").find("em").string
                except AttributeError:
                    purchased = None

                try:
                    recommendation = opinion.find(
                        "div", "product-review-summary").find("em").string
                except AttributeError:
                    recommendation = None

                try:
                    purchase_date = dates.pop(0)["datetime"]
                except IndexError:
                    purchase_date = None

                try:
                    pros = opinion.find(
                        "div", "pros-cell").find("ul").get_text()
                except AttributeError:
                    pros = None

                try:
                    cons = opinion.find(
                        "div", "cons-cell").find("ul").get_text()
                except AttributeError:
                    cons = None

                opinion_dict = {
                    "opinion_id": opinion_id,
                    "author": author,
                    "recommendation": recommendation,
                    "stars": stars,
                    "pros": pros,
                    "cons": cons,
                    "purchased": purchased,
                    "purchase_date": purchase_date,
                    "review_date": review_date,
                    "useful": useful,
                    "useless": useless,
                    # "content": content
                }

                opinions_list.append(opinion_dict)

            try:
                url = url_prefix + \
                    page_tree.find("a", "pagination__next")["href"]
            except TypeError:
                url = None

        with open(product_id+'.json', 'w', encoding="utf-8") as fp:
            json.dump(opinions_list, fp, ensure_ascii=False,
                      indent=4, separators=(',', ': '))

        # Przekierowanie na stronę produktu
        return render(request, 'scraper/single_product.html', {'opinions': opinions_list, 'product': product, 'title': 'Product'})

    # Przekierowanie na stronę ekstrakcji (czysty formularz)
    return render(request, 'scraper/extraction.html', {'title': 'Ekstrakcja opinii'})
