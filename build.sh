#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from backend directory
# pip install -r backend/requirements.txt

# Change to backend directory
cd backend

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Create demo user if it doesn't exist
python manage.py create_demo_user || true
