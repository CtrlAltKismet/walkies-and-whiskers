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
                        "Leave blank if there are none."
                    ),
                }
            ),
            "feeding_notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": (
                        "Include feeding times, portions or dietary needs or state "
                        "that there are no special feeding requirements."
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

    
    def clean_feeding_notes(self):
        """Ensure useful feeding information is provided."""
        feeding_notes = self.cleaned_date["feeding_notes"].strip()
        
        if not feeding_notes:
            raise forms.ValidationError(
                "Please provide feeding instructions or state that there "
                "are no special feeding requirements."
            )
        
        return feeding_notes