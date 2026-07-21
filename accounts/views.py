from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import RegisterForm


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