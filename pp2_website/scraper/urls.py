from django.urls import path
from . import views
from .views import ProductListView, ProductDetailView, ProductChartslView

urlpatterns = [
    path('', views.home, name='scraper-home'),
    path('author', views.author, name='scraper-author'),
    path('extraction', views.extraction, name='scraper-extraction'),
    path('products', ProductListView.as_view(), name='scraper-products'),

    # Trasy dla danych danych pobieranych bezpośrednio z ekstrakcji
    path('single-product', views.singleProduct, name='scraper-single-product'),
    path('show-charts', views.show_charts, name='show-charts'),
    path('download-opinions', views.download_file, name='download-file'),

    # Trasy dla danych danych pobieranych z bazy danych
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product-charts/<int:pk>/', ProductChartslView.as_view(), name='product-charts'),
    path('product-download', views.productDownload, name='product-download'),
]
