import os
import django
from sales.models import Product, SalesRecord
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales_dashboard.settings")
django.setup()



def seed_products():
    products = [
        {"product_name": "Laptop", "quantity_in_stock": 50},
        {"product_name": "Mobile Phone", "quantity_in_stock": 100},
        {"product_name": "Headphones", "quantity_in_stock": 75},
    ]
    
    for prod in products:
        obj, created = Product.objects.get_or_create(product_name=prod["product_name"], defaults={"quantity_in_stock": prod["quantity_in_stock"]})
        if not created:
            obj.quantity_in_stock = prod["quantity_in_stock"]
            obj.save()
        print(f"Product {obj.product_name} added.")

def seed_sales():
    if SalesRecord.objects.exists():
        print("Sales data already exists. Skipping seed.")
        return

    product = Product.objects.first()
    if not product:
        print("No products found, skipping sales data.")
        return

    sales = [
        {"customer_name": "Alice", "salesperson": "Bob", "product": product, "quantity": 2, "price_per_unit": 1000, "date_of_sale": date.today()},
        {"customer_name": "Charlie", "salesperson": "David", "product": product, "quantity": 1, "price_per_unit": 1000, "date_of_sale": date.today()},
    ]
    
    for sale in sales:
        SalesRecord.objects.create(**sale)
        print(f"Sale for {sale['customer_name']} added.")

def run():
    seed_products()
    seed_sales()

if __name__ == "__main__":
    run()
