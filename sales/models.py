from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    product_name = models.CharField(max_length=255, unique=True)
    quantity_in_stock = models.PositiveIntegerField()

    def __str__(self):
        return self.product_name

    def clean(self):
        if Product.objects.filter(product_name__iexact=self.product_name).exclude(pk=self.pk).exists():
            raise ValidationError(f"A product with the name '{self.product_name}' already exists.")

    def save(self, *args, **kwargs):
        existing = Product.objects.filter(product_name__iexact=self.product_name).exclude(pk=self.pk).first()
        if existing:
            existing.quantity_in_stock += self.quantity_in_stock
            existing.save()
            return existing
        self.full_clean()
        return super().save(*args, **kwargs)


class SalesRecord(models.Model):
    customer_name = models.CharField(max_length=255)
    salesperson = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_of_sale = models.DateField()

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.price_per_unit

        if self.pk is None:
            product = self.product
            if product.quantity_in_stock >= self.quantity:
                product.quantity_in_stock -= self.quantity
                product.save()
            else:
                raise ValueError("Not enough stock available!")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_name} - {self.product.product_name}"
