from django import forms

from .models import Pet


class PetForm(forms.ModelForm):
    """Create or update a pet profile."""

    class Meta:
        model = Pet
        fields = (
            "name",
            "species",
            "breed",
            "age",
            "size",
            "temperament",
            "medical_notes",
            "feeding_notes",
        )
        widgets = {
            "temperament": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Describe your pet's temperament and behaviour."
                    ),
                }
            ),
            "medical_notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Include allergies, medication or other care needs."
                    ),
                }
            ),
            "feeding_notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Include feeding times, portions or dietary needs."
                    ),
                }
            ),
        }

    def clean_name(self):
        """Remove unnecessary spaces from the pet's name."""
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Please enter your pet's name."
            )

        return name

    def clean_species(self):
        """Remove unnecessary spaces from the species."""
        species = self.cleaned_data["species"].strip()

        if not species:
            raise forms.ValidationError(
                "Please enter your pet's species."
            )

        return species