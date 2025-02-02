from django.shortcuts import render, redirect
from .models import SalesRecord, Product
from .forms import SalesForm, ProductForm
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .models import SalesRecord
from django.contrib import messages


def sales_list(request):
    sales = SalesRecord.objects.all()
    return render(request, 'sales/sales_list.html', {'sales': sales})

# def add_sale(request):
#     if request.method == 'POST':
#         form = SalesForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('sales_list')
#     else:
#         form = SalesForm()
#     return render(request, 'sales/add_sale.html', {'form': form})



def add_sale(request):
    if request.method == 'POST':
        form = SalesForm(request.POST)
        if form.is_valid():
            sale = form.save(commit=False)  # Don't save yet

            # Check stock availability
            product = sale.product
            if product.quantity_in_stock >= sale.quantity:
                sale.save()  # Save the sale (this also updates stock via model save method)
                messages.success(request, "Sale recorded successfully!")
                return redirect('sales_list')
            else:
                messages.error(request, "Not enough stock available!")

    else:
        form = SalesForm()

    return render(request, 'sales/add_sale.html', {'form': form})



def product_stock(request):
    products = Product.objects.all()
    return render(request, 'product_stock/products_list.html', {'products': products})

# views.py
def add_products(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                # Check if we handled existing product in clean()
                if form.has_error(None):
                    messages.info(request, form.errors['__all__'][0])
                else:
                    form.save()
                    messages.success(request, "New product created successfully!")
                return redirect('product_stock')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = ProductForm()
    
    return render(request, 'product_stock/add_product.html', {'form': form})

def dashboard(request):
    # Get filter parameters from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    salesperson = request.GET.get('salesperson')
    product_name = request.GET.get('product_name')
    
    # Start with all records
    sales_data = SalesRecord.objects.all()
    
    # Apply filters if they exist
    if start_date:
        sales_data = sales_data.filter(date_of_sale__gte=start_date)
    if end_date:
        sales_data = sales_data.filter(date_of_sale__lte=end_date)
    if salesperson:
        sales_data = sales_data.filter(salesperson=salesperson)
    if product_name:
        sales_data = sales_data.filter(product_id=product_name)

    # Determine target_date based on filters or use today
    target_date = datetime.today()  # Default to today
    if start_date:
        target_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Calculate month boundaries based on target_date
    first_day_of_month = target_date.replace(day=1)
    next_month = first_day_of_month + timedelta(days=32)
    last_day_of_month = next_month.replace(day=1) - timedelta(days=1)
    
    # Filter sales for the target month (independent of date filters)
    current_month_sales = sales_data.filter(
        date_of_sale__gte=first_day_of_month,
        date_of_sale__lte=last_day_of_month
    )

    # Aggregate data
    total_revenue = sales_data.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_sales = sales_data.count()
    
    top_products = sales_data.values('product__product_name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]

    salesperson_revenue = sales_data.values('salesperson').annotate(
        revenue=Sum('total_price')
    ).order_by('-revenue')

    # Weekly revenue calculations for the target month
    week_1_end = first_day_of_month + timedelta(days=6)
    week_2_end = first_day_of_month + timedelta(days=13)
    week_3_end = first_day_of_month + timedelta(days=20)
    
    week_1_sales = current_month_sales.filter(date_of_sale__lte=week_1_end)
    week_2_sales = current_month_sales.filter(
        date_of_sale__gt=week_1_end,
        date_of_sale__lte=week_2_end
    )
    week_3_sales = current_month_sales.filter(
        date_of_sale__gt=week_2_end,
        date_of_sale__lte=week_3_end
    )
    week_4_sales = current_month_sales.filter(date_of_sale__gt=week_3_end)

    # Calculate weekly revenues
    revenue_week_1 = week_1_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
    revenue_week_2 = week_2_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
    revenue_week_3 = week_3_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0
    revenue_week_4 = week_4_sales.aggregate(Sum('total_price'))['total_price__sum'] or 0

    # Generate week labels
    month_name = target_date.strftime('%b')
    week_labels = [
        f"1-{week_1_end.day} {month_name}",
        f"{week_1_end.day+1}-{week_2_end.day} {month_name}",
        f"{week_2_end.day+1}-{week_3_end.day} {month_name}",
        f"{week_3_end.day+1}-{last_day_of_month.day} {month_name}"
    ]

    # Prepare context
    context = {
        'total_revenue': total_revenue,
        'total_sales': total_sales,
        'top_products': top_products,
        'salespeople': SalesRecord.objects.values_list('salesperson', flat=True).distinct(),
        'products': Product.objects.all(),
        'revenue_week_1': revenue_week_1,
        'revenue_week_2': revenue_week_2,
        'revenue_week_3': revenue_week_3,
        'revenue_week_4': revenue_week_4,
        'week_labels': week_labels,
        'selected_start_date': start_date,
        'selected_end_date': end_date,
        'selected_salesperson': salesperson,
        'selected_product': product_name,
        'salesperson_revenue': salesperson_revenue,
        'total_sales_data': sales_data.values('date_of_sale').annotate(
            sales_count=Count('id')
        ).order_by('date_of_sale'),
        'low_stock_products': Product.objects.filter(quantity_in_stock__lt=5),
    }
    
    return render(request, 'sales/dashboard.html', context)