from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import ClothItem, Stock
from .serializers import ClothItemSerializer, StockSerializer, StockUpdateSerializer


class ClothItemViewSet(viewsets.ModelViewSet):
    queryset = ClothItem.objects.all()
    serializer_class = ClothItemSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    def get_queryset(self):
        queryset = ClothItem.objects.all()
        
        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by size
        size = self.request.query_params.get('size', None)
        if size:
            queryset = queryset.filter(size=size)
        
        # Search by name or SKU
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(sku__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset

    def perform_create(self, serializer):
        item = serializer.save()
        # Create stock entry for new item
        Stock.objects.create(item=item, quantity=0)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Get items with low stock"""
        low_stock_items = []
        for item in ClothItem.objects.all():
            if hasattr(item, 'stock') and item.stock.is_low_stock:
                low_stock_items.append(item)
        
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    @action(detail=False, methods=['post'])
    def update_stock(self, request):
        """Update stock quantity for an item"""
        serializer = StockUpdateSerializer(data=request.data)
        if serializer.is_valid():
            item_id = serializer.validated_data['item_id']
            quantity = serializer.validated_data['quantity']
            
            try:
                stock = Stock.objects.get(item_id=item_id)
                stock.quantity = quantity
                
                if 'low_stock_threshold' in serializer.validated_data:
                    stock.low_stock_threshold = serializer.validated_data['low_stock_threshold']
                
                stock.save()
                return Response(StockSerializer(stock).data)
            except Stock.DoesNotExist:
                return Response(
                    {'error': 'Stock not found for this item'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def adjust_stock(self, request):
        """Adjust stock by adding or subtracting quantity"""
        item_id = request.data.get('item_id')
        adjustment = request.data.get('adjustment', 0)
        
        try:
            stock = Stock.objects.get(item_id=item_id)
            new_quantity = max(0, stock.quantity + adjustment)
            stock.quantity = new_quantity
            stock.save()
            return Response(StockSerializer(stock).data)
        except Stock.DoesNotExist:
            return Response(
                {'error': 'Stock not found for this item'},
                status=status.HTTP_404_NOT_FOUND
            )
