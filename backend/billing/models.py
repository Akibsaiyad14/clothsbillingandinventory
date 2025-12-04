from django.db import models
from django.core.validators import MinValueValidator
from inventory.models import ClothItem


class Bill(models.Model):
    """Model for customer bills"""
    bill_number = models.CharField(max_length=50, unique=True)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    tax_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    final_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Bill #{self.bill_number} - {self.customer_name}"

    def calculate_totals(self):
        """Calculate total, tax, and final amount"""
        items_total = sum(item.subtotal for item in self.items.all())
        self.total_amount = items_total
        
        # Apply discount
        discount_amount = (self.total_amount * self.discount) / 100
        amount_after_discount = self.total_amount - discount_amount
        
        # Apply tax
        tax_amount = (amount_after_discount * self.tax_rate) / 100
        self.final_amount = amount_after_discount + tax_amount
        
        self.save()


class BillItem(models.Model):
    """Model for items in a bill"""
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item = models.ForeignKey(
        ClothItem,
        on_delete=models.PROTECT,
        related_name='bill_items'
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.item.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Auto-calculate subtotal
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)
