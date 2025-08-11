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

# Collect static files on first import
from django.core.management import execute_from_command_line
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
except:
    pass  # Ignore errors during static collection

# Import the WSGI application
from djblogsite.wsgi import application

# Vercel expects the WSGI application to be named 'app'
app = application