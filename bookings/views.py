from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from datetime import datetime
from django.utils import timezone

from .forms import BookingForm
from .models import Booking
from .weather import get_weather_guidance


@login_required
def booking_create(request):
    """Allow a logged-in user to create a pending booking."""

    if request.method == "POST":
        form = BookingForm(request.POST)
    else:
        form = BookingForm()

    form.fields["pet"].queryset = request.user.pets.all()
    form.fields["service"].queryset = (
        form.fields["service"].queryset.filter(is_active=True)
    )

    if request.method == "POST" and form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.status = booking.STATUS_PENDING
        booking.total_price = booking.service.price
        
        if booking.service.is_outdoor_service:
            booking.weather_summary = get_weather_guidance(
                booking.booking_date,
            )
        
        booking.save()

        messages.success(
            request,
            "Your booking has been created and is awaiting payment.",
        )

        return redirect("booking_create")

    context = {
        "form": form,
    }

    return render(
        request,
        "bookings/booking_form.html",
        context,
    )
    

@login_required
def booking_list(request):
    """Display bookings belonging to the logged-in user."""
    
    bookings = Booking.objects.filter(
        user=request.user,
    ).order_by(
        "booking_date",
        "booking_time",
    )
    
    for booking in bookings:
        booking_datetime = timezone.make_aware(
            datetime.combine(
                booking.booking_date,
                booking.booking_time,
            )
        )
        
        booking.has_passed = booking_datetime <= timezone.now()
    
    context = {
        "bookings": bookings,
    }
    
    return render(
        request,
        "bookings/booking_list.html",
        context,
    )
    

@login_required
def booking_detail(request, booking_id):
    """Display a detailed booking belonging to the logged-in user."""
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
    )
    
    booking_datetime = timezone.make_aware(
        datetime.combine(
            booking.booking_date,
            booking.booking_time,
        )
    )
    
    booking_has_passed = booking_datetime <= timezone.now()
    
    context = {
        "booking": booking,
        "booking_has_passed": booking_has_passed,
    }
    
    return render(
        request,
        "bookings/booking_detail.html",
        context,
    )
    

@login_required
def booking_cancel(request, booking_id):
    """Allow a user to cancel one of their own bookings."""
    
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
    )
    
    if request.method == "POST":
        booking.status = Booking.STATUS_CANCELLED
        
        booking.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )
        
        messages.success(
            request,
            "Your booking has been cancelled successfully.",
        )
        
        return redirect(
            "booking_detail",
            booking_id=booking.id,
        )
        
    return render(
        request,
        "bookings/booking_cancel.html",
        {
            "booking": booking,
        },
    )