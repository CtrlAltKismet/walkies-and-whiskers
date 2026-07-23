from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Configure Stripe payment records in Django Admin."""
    
    list_display = (
        "id",
        "booking",
        "user",
        "amount",
        "status",
        "stripe_checkout_id",
        "created_at",
    )
    list_filter = (
        "status",
        "created_at",
    )
    search_fields = (
        "booking__pet__name",
        "booking__service__name",
        "user__username",
        "stripe_checkout_id",
        "stripe_payment_intent",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )