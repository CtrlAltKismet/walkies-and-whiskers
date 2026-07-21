from django.contrib import admin


from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Configure Service records in Django admin."""
    
    list_display = (
        "name",
        "price",
        "duration_minutes",
        "is_outdoor_service",
        "is_active",
    )
    list_filter = ("is_active", "is_outdoor_service")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
