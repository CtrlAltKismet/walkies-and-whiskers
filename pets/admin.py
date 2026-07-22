from django.contrib import admin

from .models import Pet


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    """Configure pet profiles in Django admin."""
    
    list_display = (
        "name",
        "species",
        "breed",
        "size",
        "owner",
        "created_at",
    )
    list_filter = (
        "species",
        "size",
    )
    search_fields = (
        "name",
        "species",
        "breed",
        "owner_username",
    )