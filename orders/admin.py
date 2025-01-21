from django.contrib import admin
from .models import Order, Product

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'status', 'total_price', 'user')
    search_fields = ('customer_name', 'id')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'price', 'quantity')
    search_fields = ('name',)
