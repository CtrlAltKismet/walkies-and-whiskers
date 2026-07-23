from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from datetime import datetime
from django.utils import timezone

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
    
    booking_datetime = timezone.make_aware(
        datetime.combine(
            booking.booking_date,
            booking.booking_time,
        )
    )
    
    if booking_datetime <= timezone.now():
        messages.error(
            request,
            "This booking date has already passed and can no longer be paid.",
        )
        
        return redirect(
            "booking_detail",
            booking_id=booking.id,
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
            "payment_cancel",
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

    booking_id = checkout_session.metadata["booking_id"]

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
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

    order, created = Order.objects.update_or_create(
        stripe_checkout_id=checkout_session.id,
        defaults={
            "user": request.user,
            "booking": booking,
            "stripe_payment_intent": (
                checkout_session.payment_intent or ""
            ),
            "amount": booking.total_price,
            "status": Order.STATUS_PAID,
        },
    )

    if booking.status == Booking.STATUS_PENDING:
        booking.status = Booking.STATUS_CONFIRMED

        booking.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        
    if created:
        send_mail(
            subject="Your Walkies & Whiskers booking is confirmed",
            message=(
                f"Hello {request.user.username},\n\n"
                "Thank you for your payment. Your booking is now "
                "confirmed.\n\n"
                f"Pet: {booking.pet.name}\n"
                f"Service: {booking.service.name}\n"
                f"Date: {booking.booking_date.strftime('%d %B %Y')}\n"
                f"Time: {booking.booking_time.strftime('%H:%M')}\n"
                f"Amount paid: £{booking.total_price}\n"
                f"Status: {booking.get_status_display()}\n\n"
                "You can view the full booking details from the "
                "My Bookings section of your account.\n\n"
                "Thank you for choosing Walkies & Whiskers."
            ),
            from_email=None,
            recipient_list=[request.user.email],
            fail_silently=False,
        )

    messages.success(
        request,
        "Payment successful. Your booking is now confirmed.",
    )

    context = {
        "booking": booking,
        "order": order,
    }

    return render(
        request,
        "checkout/payment_success.html",
        context,
    )
    

@login_required
def payment_cancel(request, booking_id):
    """Show feedback after a user cancels Stripe Checkout."""
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        status=Booking.STATUS_PENDING
    )
    
    messages.info(
        request,
        "Payment was cancelled. Your booking is still awaiting payment.",
    )
    
    context = {
        "booking": booking,
    }
    
    return render(
        request,
        "checkout/payment_cancel.html",
        context,
    )
    