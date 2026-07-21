from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
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