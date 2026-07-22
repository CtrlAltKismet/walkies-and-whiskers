from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Configure bookings in Django admin."""
    
    list_display = (
        "id",
        "user",
        "pet",
        "service",
        "booking_date",
        "booking_time",
        "status",
        "total_price",
        "created_at",
    )
    list_filter = (
        "status",
        "service",
        "booking_date",
    )
    search_fields = (
        "user__username",
        "pet__name",
        "service__name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )