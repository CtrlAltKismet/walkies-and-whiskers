from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from bookings.models import Booking
from .models import Order


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
        reverse("payment_success")
    )
    
    success_url += "?session_id={CHECKOUT_SESSION_ID}"
    
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
    

@login_required
def payment_success(request):
    """Confirm a booking after verifying a successful Stripe payment."""

    session_id = request.GET.get("session_id")

    if not session_id:
        messages.error(
            request,
            "The payment could not be verified.",
        )

        return redirect("booking_list")

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        checkout_session = stripe.checkout.Session.retrieve(
            session_id,
        )
    except stripe.StripeError:
        messages.error(
            request,
            "The payment could not be verified with Stripe.",
        )

        return redirect("booking_list")

    if checkout_session.payment_status != "paid":
        messages.error(
            request,
            "Payment has not been completed.",
        )

        return redirect("booking_list")

    booking_id = checkout_session.metadata.get("booking_id")

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status=Booking.STATUS_PENDING,
    )

    expected_amount = int(
        booking.total_price * Decimal("100")
    )

    if checkout_session.amount_total != expected_amount:
        messages.error(
            request,
            "The payment amount could not be verified.",
        )

        return redirect(
            "booking_detail",
            booking_id=booking.id,
        )

    Order.objects.update_or_create(
        booking=booking,
        defaults={
            "user": request.user,
            "stripe_checkout_id": checkout_session.id,
            "stripe_payment_intent": (
                checkout_session.payment_intent or ""
            ),
            "amount": booking.total_price,
            "status": Order.STATUS_PAID,
        },
    )

    booking.status = Booking.STATUS_CONFIRMED
    booking.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Payment successful. Your booking is now confirmed.",
    )

    context = {
        "booking": booking,
        "order": booking.order,
    }

    return render(
        request,
        "checkout/payment_success.html",
        context,
    )