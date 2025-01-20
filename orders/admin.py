from django.contrib import admin
from .models import Order, Product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'status', 'total_price', 'user')
    search_fields = ('customer_name', 'order_id')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'quantity')
    search_fields = ('name', 'product_id')
