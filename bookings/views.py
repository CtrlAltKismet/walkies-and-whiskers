from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
    
    context = {
        "booking": booking,
    }
    
    return render(
        request,
        "bookings/booking_detail.html",
        context,
    )