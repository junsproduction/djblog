#!/bin/bash
set -e

echo "🚀 Build phase dimulai…"

# Install deps (Vercel udah otomatis, tapi biar aman)
python3.12 -m pip install -r requirements.txt

echo "📦 Collect static files…"
python3.12 manage.py collectstatic --noinput --clear --verbosity=1

echo "🔄 Jalankan migrasi…"
python3.12 manage.py migrate --noinput

echo "👤 Superuser (silent kalau sudah ada)…"
python3.12 manage.py create_superuser 2>/dev/null || true

echo "✅ Build selesai"