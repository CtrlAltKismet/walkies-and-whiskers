from django import forms
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
    UserCreationForm,
)
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

class CustomPasswordChangeForm(PasswordChangeForm):
    """Prevent users from reusing their current password."""
    
    def clean_new_password1(self):
        """Check that the new password differs from the old password."""
        new_password = self.cleaned_data.get("new_password1")
        
        if new_password and self.user.check_password(new_password):
            raise forms.ValidationError(
                "Your new password must be different from your current password."
            )
            
        return new_password
    
class CustomSetPasswordForm(SetPasswordForm):
    """Prevent password reuse during an email password reset."""
    
    def clean_new_password1(self):
        """Check that the new password differs from the current password."""
        new_password = self.cleaned_data.get("new_password1")
        
        if new_password and self.user.check_password(new_password):
            raise forms.ValidationError(
                "Your new password must be different from your current password."
            )
        
        return new_password