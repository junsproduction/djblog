#!/bin/bash
set -e  # exit on any error

echo "🚀  Vercel build starting…"

# 1. Install Python dependencies
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

# 2. Collect static files (output to ./staticfiles)
echo "📦  Collecting static files…"
python3.12 manage.py collectstatic --noinput --clear --verbosity=2

# 3. (Optional) run migrations if your DB lives on Vercel
python3.12 manage.py migrate --noinput

echo "✅  Build complete"