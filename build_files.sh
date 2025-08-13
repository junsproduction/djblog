#!/bin/bash
set -e

echo "🚀  Vercel build starting…"

# Make sure we use the correct Python interpreter
export PATH="/opt/python3.12/bin:$PATH"

# Install dependencies
python3.12 -m pip install --upgrade pip
python3.12 -m pip install -r requirements.txt

# Collect static files
echo "📦  Collecting static files…"
python3.12 manage.py collectstatic --noinput --clear --verbosity=2

# Run migrations if your DB lives on Vercel
python3.12 manage.py migrate --noinput

echo "✅  Build complete"