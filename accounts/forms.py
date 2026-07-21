from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """Create a new Walkies & Whiskers user account."""
    
    
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
