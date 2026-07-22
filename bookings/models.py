from django.conf import settings
from django.db import models

from pets.models import Pet
from services.models import Service


class Booking(models.Model):
    """Store a pet-care booking created by a registered user."""
    
    STATUS_PENDING = "pending_payment"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending payment"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    booking_date = models.DateField()
    booking_time = models.TimeField()
    notes = models.TextField(
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    weather_summary = models.TextField(
        blank=True,
    )
    total_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    
    class Meta:
        ordering = [
            "booking_date",
            "booking_time",
        ]
        
    def __str__(self):
        """Return a readable booking description."""
        return (
            f"{self.pet.name} - "
            f"{self.service.name} - "
            f"{self.booking_date}"
        )