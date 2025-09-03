import os
import sys
from pathlib import Path

# Configure paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djblogsite.settings')

# Setup error handling
try:
    import django
    django.setup()
    
    # Try importing the problematic modules first
    from blog.storage import VercelBlobStorage
    from djblogsite.wsgi import application
    
    app = application

except ImportError as e:
    # Log the error
    print(f"Import Error: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    print(f"Installed packages:", file=sys.stderr)
    from importlib.metadata import distributions
    for pkg in distributions():
        print(f"  - {pkg.metadata['Name']} {pkg.version}", file=sys.stderr)
    raise

except Exception as e:
    print(f"Unexpected error: {e}", file=sys.stderr)
    raise