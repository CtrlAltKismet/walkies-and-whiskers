from django import forms
from django.utils import timezone

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

    def clean(self):
        """Prevent bookings from being created in the past."""
        cleaned_data = super().clean()

        booking_date = cleaned_data.get("booking_date")
        booking_time = cleaned_data.get("booking_time")

        today = timezone.localdate()
        current_time = timezone.localtime().time()

        if booking_date and booking_date < today:
            self.add_error(
                "booking_date",
                "Please choose today or a future date.",
            )

        if (
            booking_date
            and booking_time
            and booking_date == today
            and booking_time <= current_time
        ):
            self.add_error(
                "booking_time",
                "Please choose a time later than the current time.",
            )

        return cleaned_data