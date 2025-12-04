from django.core.management.base import BaseCommand
from inventory.models import ClothItem, Stock


class Command(BaseCommand):
    help = 'Populate database with sample cloth items'

    def handle(self, *args, **kwargs):
        sample_items = [
            # T-Shirts
            {
                'name': 'Cotton T-Shirt',
                'category': 'TSHIRT',
                'size': 'M',
                'color': 'White',
                'price': 15.99,
                'sku': 'TSH-WHT-M-001',
                'description': 'Comfortable cotton t-shirt for everyday wear',
                'stock': 50
            },
            {
                'name': 'Cotton T-Shirt',
                'category': 'TSHIRT',
                'size': 'L',
                'color': 'Black',
                'price': 15.99,
                'sku': 'TSH-BLK-L-001',
                'description': 'Comfortable cotton t-shirt for everyday wear',
                'stock': 45
            },
            {
                'name': 'V-Neck T-Shirt',
                'category': 'TSHIRT',
                'size': 'M',
                'color': 'Navy Blue',
                'price': 17.99,
                'sku': 'TSH-NVY-M-002',
                'description': 'Stylish v-neck t-shirt',
                'stock': 30
            },
            {
                'name': 'Graphic T-Shirt',
                'category': 'TSHIRT',
                'size': 'XL',
                'color': 'Red',
                'price': 19.99,
                'sku': 'TSH-RED-XL-003',
                'description': 'Trendy graphic print t-shirt',
                'stock': 25
            },
            
            # Shirts
            {
                'name': 'Formal Dress Shirt',
                'category': 'SHIRT',
                'size': 'M',
                'color': 'White',
                'price': 35.99,
                'sku': 'SHT-WHT-M-001',
                'description': 'Classic white formal shirt',
                'stock': 40
            },
            {
                'name': 'Formal Dress Shirt',
                'category': 'SHIRT',
                'size': 'L',
                'color': 'Light Blue',
                'price': 35.99,
                'sku': 'SHT-BLU-L-001',
                'description': 'Professional light blue shirt',
                'stock': 35
            },
            {
                'name': 'Casual Check Shirt',
                'category': 'SHIRT',
                'size': 'M',
                'color': 'Blue Check',
                'price': 29.99,
                'sku': 'SHT-CHK-M-002',
                'description': 'Casual checkered shirt',
                'stock': 28
            },
            {
                'name': 'Oxford Shirt',
                'category': 'SHIRT',
                'size': 'L',
                'color': 'Pink',
                'price': 32.99,
                'sku': 'SHT-PNK-L-003',
                'description': 'Smart casual oxford shirt',
                'stock': 20
            },
            
            # Pants
            {
                'name': 'Formal Trousers',
                'category': 'PANTS',
                'size': '32',
                'color': 'Black',
                'price': 45.99,
                'sku': 'PNT-BLK-32-001',
                'description': 'Classic black formal trousers',
                'stock': 30
            },
            {
                'name': 'Formal Trousers',
                'category': 'PANTS',
                'size': '34',
                'color': 'Grey',
                'price': 45.99,
                'sku': 'PNT-GRY-34-001',
                'description': 'Professional grey trousers',
                'stock': 25
            },
            {
                'name': 'Chino Pants',
                'category': 'PANTS',
                'size': '32',
                'color': 'Khaki',
                'price': 39.99,
                'sku': 'PNT-KHK-32-002',
                'description': 'Casual khaki chino pants',
                'stock': 35
            },
            {
                'name': 'Cotton Pants',
                'category': 'PANTS',
                'size': '34',
                'color': 'Navy',
                'price': 42.99,
                'sku': 'PNT-NVY-34-003',
                'description': 'Comfortable cotton pants',
                'stock': 22
            },
            
            # Jeans
            {
                'name': 'Slim Fit Jeans',
                'category': 'JEANS',
                'size': '32',
                'color': 'Dark Blue',
                'price': 49.99,
                'sku': 'JNS-DBL-32-001',
                'description': 'Modern slim fit jeans',
                'stock': 40
            },
            {
                'name': 'Slim Fit Jeans',
                'category': 'JEANS',
                'size': '34',
                'color': 'Light Blue',
                'price': 49.99,
                'sku': 'JNS-LBL-34-001',
                'description': 'Casual light wash jeans',
                'stock': 38
            },
            {
                'name': 'Regular Fit Jeans',
                'category': 'JEANS',
                'size': '32',
                'color': 'Black',
                'price': 52.99,
                'sku': 'JNS-BLK-32-002',
                'description': 'Classic black jeans',
                'stock': 32
            },
            {
                'name': 'Skinny Jeans',
                'category': 'JEANS',
                'size': '30',
                'color': 'Grey',
                'price': 47.99,
                'sku': 'JNS-GRY-30-003',
                'description': 'Trendy skinny fit jeans',
                'stock': 15
            },
            
            # Jackets
            {
                'name': 'Denim Jacket',
                'category': 'JACKET',
                'size': 'M',
                'color': 'Blue',
                'price': 79.99,
                'sku': 'JKT-BLU-M-001',
                'description': 'Classic denim jacket',
                'stock': 18
            },
            {
                'name': 'Leather Jacket',
                'category': 'JACKET',
                'size': 'L',
                'color': 'Black',
                'price': 149.99,
                'sku': 'JKT-BLK-L-001',
                'description': 'Premium leather jacket',
                'stock': 12
            },
            {
                'name': 'Bomber Jacket',
                'category': 'JACKET',
                'size': 'M',
                'color': 'Olive Green',
                'price': 89.99,
                'sku': 'JKT-OLV-M-002',
                'description': 'Military style bomber jacket',
                'stock': 8
            },
            
            # Sweaters
            {
                'name': 'Wool Sweater',
                'category': 'SWEATER',
                'size': 'M',
                'color': 'Navy',
                'price': 59.99,
                'sku': 'SWT-NVY-M-001',
                'description': 'Warm wool sweater',
                'stock': 25
            },
            {
                'name': 'Cardigan',
                'category': 'SWEATER',
                'size': 'L',
                'color': 'Grey',
                'price': 54.99,
                'sku': 'SWT-GRY-L-001',
                'description': 'Comfortable cardigan',
                'stock': 20
            },
            {
                'name': 'Hoodie',
                'category': 'SWEATER',
                'size': 'M',
                'color': 'Black',
                'price': 44.99,
                'sku': 'SWT-BLK-M-002',
                'description': 'Casual pullover hoodie',
                'stock': 35
            },
        ]

        created_count = 0
        updated_count = 0

        for item_data in sample_items:
            stock_quantity = item_data.pop('stock')
            
            # Check if item already exists
            item, created = ClothItem.objects.get_or_create(
                sku=item_data['sku'],
                defaults=item_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created: {item.name} - {item.sku}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'Already exists: {item.name} - {item.sku}'))
            
            # Create or update stock
            stock, stock_created = Stock.objects.get_or_create(
                item=item,
                defaults={'quantity': stock_quantity, 'low_stock_threshold': 10}
            )
            
            if not stock_created:
                stock.quantity = stock_quantity
                stock.save()

        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} new items'))
        self.stdout.write(self.style.SUCCESS(f'Found {updated_count} existing items'))
        self.stdout.write(self.style.SUCCESS(f'Total items in database: {ClothItem.objects.count()}'))
