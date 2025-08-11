from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser automatically (with debug output)'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get superuser credentials from environment variables
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('SUPERUSER_PASSWORD', 'admin123')
        full_name = os.environ.get('SUPERUSER_FULL_NAME', 'Admin User')

        self.stdout.write(self.style.NOTICE(f"[DEBUG] SUPERUSER_EMAIL: {email}"))
        self.stdout.write(self.style.NOTICE(f"[DEBUG] SUPERUSER_FULL_NAME: {full_name}"))
        self.stdout.write(self.style.NOTICE(f"[DEBUG] SUPERUSER_PASSWORD: {'*' * len(password)} (hidden)"))

        # Check if superuser already exists (by email)
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser with email "{email}" already exists.')
            )
            return
        
        # Create superuser
        try:
            User.objects.create_superuser(
                email=email,
                password=password,
                full_name=full_name
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{email}" created successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
