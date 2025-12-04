#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from backend directory
pip install --upgrade pip
pip install -r backend/requirements.txt

# Change to backend directory
cd backend

# Collect static files (with minimal output)
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate --no-input

# Create demo user if it doesn't exist
echo "Creating demo user..."
python manage.py create_demo_user || true

echo "Build completed successfully!"
