# Quick Setup Script for Cloth Shop Management System
# Run this in PowerShell after installing Python and PostgreSQL

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Cloth Shop Management System - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL
Write-Host "Checking PostgreSQL..." -ForegroundColor Yellow
$pgPath = "C:\Program Files\PostgreSQL\16\bin\psql.exe"
if (Test-Path $pgPath) {
    Write-Host "✓ PostgreSQL found" -ForegroundColor Green
} else {
    Write-Host "⚠ PostgreSQL not found at default location" -ForegroundColor Yellow
    Write-Host "  Download from: https://www.postgresql.org/download/" -ForegroundColor Yellow
}

# Navigate to backend
Set-Location -Path "backend"

# Create virtual environment
Write-Host "`nCreating virtual environment..." -ForegroundColor Yellow
python -m venv venv
Write-Host "✓ Virtual environment created" -ForegroundColor Green

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install requirements
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check .env file
Write-Host "`nChecking configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file exists" -ForegroundColor Green
} else {
    Write-Host "⚠ .env file not found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠ IMPORTANT: Edit .env file with your credentials!" -ForegroundColor Red
    Write-Host "  - PostgreSQL password" -ForegroundColor Yellow
    Write-Host "  - Email settings (for Gmail app password)" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter after updating .env file"
}

# Create database
Write-Host "`nCreating PostgreSQL database..." -ForegroundColor Yellow
try {
    python manage.py create_database
    Write-Host "✓ Database created" -ForegroundColor Green
} catch {
    Write-Host "⚠ Database creation failed. You may need to create it manually:" -ForegroundColor Yellow
    Write-Host "  psql -U postgres -c 'CREATE DATABASE clothshop_db;'" -ForegroundColor Yellow
}

# Run migrations
Write-Host "`nRunning migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate
Write-Host "✓ Migrations completed" -ForegroundColor Green

# Create demo user
Write-Host "`nCreating demo user..." -ForegroundColor Yellow
python manage.py create_demo_user
Write-Host "✓ Demo user created (username: demo, password: demo1234)" -ForegroundColor Green

# Populate sample data
Write-Host "`nPopulating sample data..." -ForegroundColor Yellow
$populate = Read-Host "Do you want to add sample cloth items? (y/n)"
if ($populate -eq 'y') {
    python manage.py populate_items
    Write-Host "✓ Sample data added" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the server:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then visit:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/login/" -ForegroundColor Cyan
Write-Host ""
Write-Host "Demo Credentials:" -ForegroundColor Yellow
Write-Host "  Username: demo" -ForegroundColor Cyan
Write-Host "  Password: demo1234" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to start server now
$start = Read-Host "Start server now? (y/n)"
if ($start -eq 'y') {
    python manage.py runserver
}
