from django.urls import path
from . import views
from .views import ProductListView, ProductDetailView

urlpatterns = [
    path('', views.home, name='scraper-home'),
    path('author', views.author, name='scraper-author'),
    path('extraction', views.extraction, name='scraper-extraction'),
    path('products', ProductListView.as_view(), name='scraper-products'),
    path('single-product', views.singleProduct, name='scraper-single-product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('download-opinions', views.download_file, name='download-file'),
    path('show-charts', views.show_charts, name='show-charts'),
]
