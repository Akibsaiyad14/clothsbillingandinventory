from rest_framework import serializers
from .models import Bill, BillItem
from inventory.serializers import ClothItemSerializer


class BillItemSerializer(serializers.ModelSerializer):
    item_details = ClothItemSerializer(source='item', read_only=True)
    item_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BillItem
        fields = ['id', 'item_id', 'item', 'item_details', 'quantity', 
                  'unit_price', 'subtotal']
        read_only_fields = ['subtotal']


class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = ['id', 'bill_number', 'customer_name', 'customer_phone', 
                  'customer_email', 'created_at', 'total_amount', 'discount', 
                  'tax_rate', 'final_amount', 'notes', 'items']
        read_only_fields = ['total_amount', 'final_amount']


class CreateBillSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=200)
    customer_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    customer_email = serializers.EmailField(required=False, allow_blank=True)
    discount = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_rate = serializers.DecimalField(max_digits=5, decimal_places=2, default=0)
    notes = serializers.CharField(required=False, allow_blank=True)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.CharField()
        )
    )

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item is required")
        
        for item in items:
            if 'item_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError(
                    "Each item must have 'item_id' and 'quantity'"
                )
        
        return items
