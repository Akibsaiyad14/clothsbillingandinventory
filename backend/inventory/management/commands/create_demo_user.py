from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a demo user for quick login testing'

    def handle(self, *args, **options):
        username = 'admin'
        password = 'admin123'
        email = 'demo@example.com'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists'))
            return

        User.objects.create_user(username=username, password=password, email=email)
        self.stdout.write(self.style.SUCCESS(f'Created demo user: {username} / {password}'))
