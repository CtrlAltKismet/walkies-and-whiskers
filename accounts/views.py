from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from bookings.models import Booking
from pets.models import Pet

from .forms import CustomPasswordChangeForm, RegisterForm


def anonymous_required(view_function):
    """Prevent logged-in users from viewing anonymous-only pages."""
    return user_passes_test(
        lambda user: not user.is_authenticated,
        login_url="home",
    )(view_function)


@anonymous_required
def register(request):
    """Allow an anonymous visitor to create an account."""
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            send_mail(
                subject="Welcome to Walkies & Whiskers",
                message=(
                    f"Hello {user.username},\n\n"
                    "Your Walkies & Whiskers account has been "
                    "created successfully.\n\n"
                    "You can now add pet profiles and book "
                    "pet-care services."
                ),
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Your account has been created successfully.",
            )

            return redirect("home")
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/register.html", context)


class CustomLoginView(auth_views.LoginView):
    """Log users in and display a confirmation message."""

    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Display a success message after a valid login."""
        response = super().form_valid(form)

        messages.success(
            self.request,
            f"Welcome back, {self.request.user.username}!",
        )

        return response


class CustomLogoutView(auth_views.LogoutView):
    """Log users out and display a confirmation message."""

    def post(self, request, *args, **kwargs):
        """Display a success message after logout."""
        response = super().post(request, *args, **kwargs)

        messages.success(
            request,
            "You have been logged out successfully.",
        )

        return response
    
    
class CustomPasswordChangeView(auth_views.PasswordChangeView):
    """Allow a logged-in user to change their password."""
    
    template_name = "accounts/password_change.html"
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    
    def form_valid(self, form):
        """Display a success message after changing the password."""
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            "Your password has been changed successfully."
        )
        
        return response
    

@login_required
def dashboard(request):
    """Display the logged-in user's account dashboard."""
    
    pet_count = Pet.objects.filter(
        owner=request.user,
    ).count()
    
    booking_count = Booking.objects.filter(
        user=request.user,
    ).count()
    
    pending_booking_count = Booking.objects.filter(
        user=request.user,
        status=Booking.STATUS_PENDING,
    ).count()
    
    upcoming_bookings = Booking.objects.filter(
        user=request.user,
        status=Booking.STATUS_CONFIRMED,
        booking_date__gte=timezone.localdate(),
    ).order_by(
        "booking_date",
        "booking_time",
    )[:3]
    
    context= {
        "pet_count": pet_count,
        "booking_count": booking_count,
        "pending_booking_count": pending_booking_count,
        "upcoming_bookings": upcoming_bookings,
    }
    
    return render(
        request,
        "accounts/dashboard.html",
        context,
    )