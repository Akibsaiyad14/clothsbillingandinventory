from django.db import models
from django.core.validators import MinValueValidator


class ClothCategory(models.TextChoices):
    SHIRT = 'SHIRT', 'Shirt'
    TSHIRT = 'TSHIRT', 'T-Shirt'
    PANTS = 'PANTS', 'Pants'
    JEANS = 'JEANS', 'Jeans'
    JACKET = 'JACKET', 'Jacket'
    SWEATER = 'SWEATER', 'Sweater'


class Size(models.TextChoices):
    XS = 'XS', 'Extra Small'
    S = 'S', 'Small'
    M = 'M', 'Medium'
    L = 'L', 'Large'
    XL = 'XL', 'Extra Large'
    XXL = 'XXL', 'Double Extra Large'


class ClothItem(models.Model):
    """Model for cloth items in the shop"""
    name = models.CharField(max_length=200)
    category = models.CharField(
        max_length=20,
        choices=ClothCategory.choices,
        default=ClothCategory.TSHIRT
    )
    size = models.CharField(
        max_length=5,
        choices=Size.choices,
        default=Size.M
    )
    color = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clothItems'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'size']),
            models.Index(fields=['sku']),
        ]

    def __str__(self):
        return f"{self.name} - {self.get_category_display()} ({self.size})"


class Stock(models.Model):
    """Model to manage inventory stock levels"""
    item = models.OneToOneField(
        ClothItem,
        on_delete=models.CASCADE,
        related_name='stock'
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    low_stock_threshold = models.IntegerField(default=10)
    last_restocked = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'stockLevels'

    def __str__(self):
        return f"{self.item.name} - Stock: {self.quantity}"

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        return self.quantity == 0
