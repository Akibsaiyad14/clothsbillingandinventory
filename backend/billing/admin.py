from django.contrib import admin
from .models import Bill, BillItem


class BillItemInline(admin.TabularInline):
    model = BillItem
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_number', 'customer_name', 'total_amount', 'final_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['bill_number', 'customer_name', 'customer_phone']
    inlines = [BillItemInline]


@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ['bill', 'item', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['bill__created_at']
