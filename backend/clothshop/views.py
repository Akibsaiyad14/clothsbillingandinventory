from django.shortcuts import render

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

def login(request):
    """Login page"""
    return render(request, 'login.html')
