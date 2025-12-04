from django.contrib import admin
from .models import ClothItem, Stock


@admin.register(ClothItem)
class ClothItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'size', 'color', 'price', 'sku', 'created_at']
    list_filter = ['category', 'size', 'color']
    search_fields = ['name', 'sku', 'description']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'is_low_stock', 'is_out_of_stock', 'last_restocked']
    list_filter = ['last_restocked']
    search_fields = ['item__name', 'item__sku']
