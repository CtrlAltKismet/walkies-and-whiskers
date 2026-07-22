from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    """Create a pet-care booking."""
    
    class Meta:
        model = Booking
        fields = (
            "pet",
            "service",
            "booking_date",
            "booking_time",
            "notes",
        )
        widgets = {
            "booking_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "booking_time": forms.TimeInput(
                attrs={
                    "type": "time",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Add any extra information for this booking. "
                        "This field is optional."
                    ),
                }
            ),
        }