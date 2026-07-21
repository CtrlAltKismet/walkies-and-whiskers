from django.shortcuts import render

from .models import Service


def service_list(request):
    """Display all active pet-care services."""
    services = Service.objects.filter(is_active=True)
    
    context = {
        "services": services,
    }
    
    return render(request, "services/service_list.html", context)