from rest_framework import serializers
from .models import ClothItem, Stock


class StockSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.ReadOnlyField()
    is_out_of_stock = serializers.ReadOnlyField()

    class Meta:
        model = Stock
        fields = ['id', 'quantity', 'low_stock_threshold', 'last_restocked', 
                  'is_low_stock', 'is_out_of_stock']


class ClothItemSerializer(serializers.ModelSerializer):
    stock = StockSerializer(read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    size_display = serializers.CharField(source='get_size_display', read_only=True)

    class Meta:
        model = ClothItem
        fields = ['id', 'name', 'category', 'category_display', 'size', 'size_display',
                  'color', 'price', 'description', 'sku', 'stock', 'created_at', 'updated_at']


class StockUpdateSerializer(serializers.Serializer):
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)
    low_stock_threshold = serializers.IntegerField(min_value=0, required=False)
