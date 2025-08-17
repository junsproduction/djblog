#!/usr/bin/env bash
set -e

echo "🚀 Install deps"
pip install -r requirements.txt

echo "📦 Collect static"
python manage.py collectstatic --noinput --clear

echo "🔄 Migrate DB"
python manage.py migrate --noinput

echo "👤 Superuser (silent)"
python manage.py create_superuser 2>/dev/null || true