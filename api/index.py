import os
import sys
from pathlib import Path

# Add the project directory to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djblogsite.settings')

# Import Django and configure
import django
django.setup()

# Run migrations and collect static files on first import
from django.core.management import execute_from_command_line
try:
    # Run migrations
    execute_from_command_line(['manage.py', 'migrate', '--noinput'])
    print("✅ Migrations completed successfully")
except Exception as e:
    print(f"❌ Migration error: {e}")

try:
    # Collect static files
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
    print("✅ Static files collected successfully")
except Exception as e:
    print(f"❌ Static files error: {e}")

# Import the WSGI application
from djblogsite.wsgi import application

# Vercel expects the WSGI application to be named 'app'
app = application