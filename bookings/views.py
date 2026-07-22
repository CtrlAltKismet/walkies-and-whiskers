from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import BookingForm


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