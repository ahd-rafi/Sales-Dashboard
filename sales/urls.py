from django.urls import path
from .views import sales_list, add_sale, dashboard, product_stock, add_products

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('sales/', sales_list, name='sales_list'),
    path('sales/add/', add_sale, name='add_sale'),
    path('stocks', product_stock, name='product_stock'),
    path('stocks/add_product', add_products, name='add_products')

]
