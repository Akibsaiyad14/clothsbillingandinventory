from django.shortcuts import render, redirect

def login(request):
    """Login page - accessible to all"""
    return render(request, 'login.html')

def dashboard(request):
    """Dashboard page"""
    return render(request, 'dashboard.html')

def inventory(request):
    """Inventory management page"""
    return render(request, 'inventory.html')

def billing(request):
    """Billing page"""
    return render(request, 'billing.html')

def reports(request):
    """Reports page"""
    return render(request, 'reports.html')
