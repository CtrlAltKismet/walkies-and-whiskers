from django.conf import settings
from django.db import models

from bookings.models import Booking


class Order(models.Model):
    """Store Stripe payment details for a booking."""
    
    STATUS_PAID = "paid"
    STATUS_PENDING = "pending"
    STATUS_FAILED = "failed"
    
    STATUS_CHOICES = [
        (STATUS_PAID, "Paid"),
        (STATUS_PENDING, "Pending"),
        (STATUS_FAILED, "Failed"),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    booking = models.OneToONeField(
        Booking,
        on_delete=models.PROTECT,
        related_name="order",
    )
    stripe_checkout_id = models.CharField(
        max_length=255,
        unique=True,
    )
    stripe_payment_intent = models.CharField(
        max_length=255,
        blanke=True,
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    class Meta:
        ordering = ["-created_at"]
        
    def __str__(self):
        """Return a readable order description."""
        return (
            f"Order for booking {self.booking.id} "
            f"({self.get_status_display()})"
        )