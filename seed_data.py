import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales_dashboard.settings")
django.setup()

from sales.models import Product, SalesRecord
from datetime import date

def seed_products():
    products = [
    {"product_name": "Laptop", "quantity_in_stock": 15},
    {"product_name": "Mobile", "quantity_in_stock": 20},
    {"product_name": "Headphones", "quantity_in_stock": 25},
    {"product_name": "Tablet", "quantity_in_stock": 4},
    {"product_name": "Smartwatch", "quantity_in_stock": 2},
    {"product_name": "Speaker", "quantity_in_stock": 8},
    {"product_name": "Keyboard", "quantity_in_stock": 12},

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

    sales_data = [
    {"customer_name": "Alice", "salesperson": "Bob", "product_name": "Laptop", "quantity": 2, "price_per_unit": 1000, "date_of_sale": "2025-02-01"},
    {"customer_name": "Charlie", "salesperson": "David", "product_name": "Mobile", "quantity": 1, "price_per_unit": 800, "date_of_sale": "2025-02-02"},
    {"customer_name": "Eve", "salesperson": "Frank", "product_name": "Headphones", "quantity": 3, "price_per_unit": 200, "date_of_sale": "2025-02-02"},
    {"customer_name": "Grace", "salesperson": "Hannah", "product_name": "Tablet", "quantity": 1, "price_per_unit": 500, "date_of_sale": "2025-02-04"},
    {"customer_name": "Isaac", "salesperson": "Bob", "product_name": "Smartwatch", "quantity": 2, "price_per_unit": 300, "date_of_sale": "2025-02-05"},
    {"customer_name": "Jane", "salesperson": "Hannah", "product_name": "Speaker", "quantity": 1, "price_per_unit": 150, "date_of_sale": "2025-01-31"},
    {"customer_name": "Liam", "salesperson": "Frank", "product_name": "Laptop", "quantity": 1, "price_per_unit": 1000, "date_of_sale": "2025-01-25"},
    {"customer_name": "Noah", "salesperson": "David", "product_name": "Mobile", "quantity": 2, "price_per_unit": 800, "date_of_sale": "2025-01-15"},

    ]

    for sale in sales_data:
        product_instance = Product.objects.filter(product_name=sale["product_name"]).first()
        if not product_instance:
            print(f"Product '{sale['product_name']}' not found, skipping this sale.")
            continue
        
        SalesRecord.objects.create(
            customer_name=sale["customer_name"],
            salesperson=sale["salesperson"],
            product=product_instance,  # Assign the correct Product instance
            quantity=sale["quantity"],
            price_per_unit=sale["price_per_unit"],
            date_of_sale=sale["date_of_sale"],
        )
        print(f"Sale for {sale['customer_name']} - {sale['product_name']} added.")


def run():
    seed_products()
    seed_sales()

if __name__ == "__main__":
    run()
