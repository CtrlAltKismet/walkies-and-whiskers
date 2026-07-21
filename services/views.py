from django.shortcuts import get_object_or_404, render

from .models import Service


def service_list(request):
    """Display all active pet-care services."""
    services = Service.objects.filter(is_active=True)
    
    context = {
        "services": services,
    }
    
    return render(request, "services/service_list.html", context)


def service_detail(request, slug):
    """Display details for one active pet-care service."""
    service = get_object_or_404(
        Service,
        slug=slug,
        is_active=True,
    )
    
    
    context = {
        "service": service,
    }
    
    
    return render(request, "services/service_detail.html", context)