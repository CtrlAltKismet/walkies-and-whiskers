from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from bookings.models import Booking


@login_required
def create_checkout_session(request, booking_id):
    """Create a Stripe Checkout Session for a pending booking."""
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status=Booking.STATUS_PENDING,
    )
    
    if request.method != "POST":
        messages.error(
            request,
            "Please use the Pay Now button to begin checkout.",
        )
        
        return redirect(
            "booking_detail",
            booking_id=booking.id,
        )
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    amount_in_pence = int(
        booking.total_price * Decimal("100")
    )
    
    success_url = request.build_absolute_uri(
        reverse(
            "booking_detail",
            kwargs={
                "booking_id": booking.id,
            },
        )
    )
    
    cancel_url = request.build_absolute_uri(
        reverse(
            "booking_detail",
            kwargs={
                "booking_id": booking.id,
            },
        )
    )
    
    checkout_session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "unit_amount": amount_in_pence,
                    "product_data": {
                        "name": booking.service.name,
                        "description": (
                            f"Pet-care booking for "
                            f"{booking.pet.name}"
                        ),
                    },
                },
                "quantity": 1,
            },
        ],
        metadata={
            "booking_id": str(booking.id),
            "user_id": str(request.user.id),
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )
    
    return redirect(
        checkout_session.url,
        code=303,
    )