from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import Bill, BillItem
from .serializers import BillSerializer, CreateBillSerializer
from inventory.models import ClothItem, Stock
import random
import string


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all actions

    def get_queryset(self):
        queryset = Bill.objects.all()
        
        # Filter by customer name
        customer = self.request.query_params.get('customer', None)
        if customer:
            queryset = queryset.filter(customer_name__icontains=customer)
        
        # Filter by date range
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if date_from:
            # Convert date string to datetime at start of day
            try:
                date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
                queryset = queryset.filter(created_at__gte=date_from_dt)
            except ValueError:
                pass
        
        if date_to:
            # Convert date string to datetime at end of day
            try:
                date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')
                # Add one day and filter less than (to include entire day)
                date_to_dt = date_to_dt + timedelta(days=1)
                queryset = queryset.filter(created_at__lt=date_to_dt)
            except ValueError:
                pass
        
        return queryset

    @transaction.atomic
    def create(self, request):
        """Create a new bill with items"""
        serializer = CreateBillSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        
        # Generate unique bill number
        bill_number = self._generate_bill_number()
        
        # Create bill
        bill = Bill.objects.create(
            bill_number=bill_number,
            customer_name=data['customer_name'],
            customer_phone=data.get('customer_phone', ''),
            customer_email=data.get('customer_email', ''),
            discount=data.get('discount', 0),
            tax_rate=data.get('tax_rate', 0),
            notes=data.get('notes', '')
        )
        
        # Create bill items and update stock
        for item_data in data['items']:
            try:
                cloth_item = ClothItem.objects.get(id=item_data['item_id'])
                quantity = int(item_data['quantity'])
                
                # Check stock availability
                if hasattr(cloth_item, 'stock'):
                    if cloth_item.stock.quantity < quantity:
                        transaction.set_rollback(True)
                        return Response(
                            {'error': f'Insufficient stock for {cloth_item.name}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )
                    
                    # Reduce stock
                    cloth_item.stock.quantity -= quantity
                    cloth_item.stock.save()
                
                # Create bill item
                BillItem.objects.create(
                    bill=bill,
                    item=cloth_item,
                    quantity=quantity,
                    unit_price=cloth_item.price
                )
            
            except ClothItem.DoesNotExist:
                transaction.set_rollback(True)
                return Response(
                    {'error': f'Item with id {item_data["item_id"]} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Calculate totals
        bill.calculate_totals()
        
        # Send email with PDF if customer email is provided
        if bill.customer_email:
            try:
                from .pdf_generator import generate_bill_pdf
                from .email_utils import send_bill_email
                
                pdf_content = generate_bill_pdf(bill)
                email_sent = send_bill_email(bill, pdf_content)
                
                response_data = BillSerializer(bill).data
                response_data['email_sent'] = email_sent
                
                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log error but still return success for bill creation
                print(f"Email sending failed: {str(e)}")
        
        return Response(
            BillSerializer(bill).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def download_pdf(self, request, pk=None):
        """Generate and download PDF for a bill"""
        from .pdf_generator import generate_bill_pdf
        
        bill = self.get_object()
        pdf_buffer = generate_bill_pdf(bill)
        
        response = HttpResponse(pdf_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="bill_{bill.bill_number}.pdf"'
        
        return response

    def _generate_bill_number(self):
        """Generate unique bill number"""
        date_str = timezone.now().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"BILL-{date_str}-{random_str}"
