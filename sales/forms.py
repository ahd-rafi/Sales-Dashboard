# from django import forms
# from .models import SalesRecord, Product

# class SalesForm(forms.ModelForm):
#     class Meta:
#         model = SalesRecord
#         fields = ['customer_name', 'salesperson', 'product_name', 'quantity', 'price_per_unit', 'date_of_sale']



# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['product_name', 'quantity_in_stock']



from django import forms
from .models import SalesRecord, Product

class SalesForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(quantity_in_stock__gt=0),  # Only show products with stock
        empty_label="Select a product"
    )

    class Meta:
        model = SalesRecord
        fields = ['customer_name', 'salesperson', 'product', 'quantity', 'price_per_unit', 'date_of_sale']

    # Optionally, add validation for fields like quantity, price_per_unit, etc.
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity

    def clean_price_per_unit(self):
        price = self.cleaned_data.get('price_per_unit')
        if price <= 0:
            raise forms.ValidationError("Price per unit must be a positive number.")
        return price


# forms.py
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'quantity_in_stock']

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        quantity = cleaned_data.get('quantity_in_stock')

        if product_name and quantity is not None:
            # Clean and normalize the product name
            product_name = product_name.strip().lower()
            
            # Check for existing product (case-insensitive)
            existing = Product.objects.filter(product_name__iexact=product_name).first()
            if existing:
                # Update existing product's stock directly
                existing.quantity_in_stock += quantity
                existing.save()
                
                # Add non-field error and prevent new creation
                self.add_error(None, f"Updated existing product stock to {existing.quantity_in_stock}")
                cleaned_data['product_name'] = existing.product_name  # Match case

        return cleaned_data

    def clean_quantity_in_stock(self):
        quantity = self.cleaned_data['quantity_in_stock']
        if quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative")
        return quantity