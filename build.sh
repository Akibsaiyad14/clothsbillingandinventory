#!/usr/bin/env bash
# exit on error
set -o errexit

cd backend

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create demo user if it doesn't exist
python manage.py create_demo_user || true
