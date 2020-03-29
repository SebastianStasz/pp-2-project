from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='scraper-home'),
    path('author', views.author, name='scraper-author'),
    path('extraction', views.extraction, name='scraper-extraction'),
    path('products', views.products, name='scraper-products'),
    path('single-product', views.singleProduct, name='scraper-single-product'),
    path('download-opinions', views.download_file, name='download-file'),
]
