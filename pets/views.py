from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PetForm


@login_required
def pet_create(request):
    """Allow a logged-in user to create a pet profile."""
    
    if request.method == "POST":
        form = PetForm(request.POST)
        
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            
            messages.success(
                request,
                f"{pet.name}'s profile has been created successfully.",
            )
            
            return redirect("pet_create")

    else:
        form = PetForm()
    
    context = {
        "form": form,
    }
    
    return render(request, "pets/pet_form.html", context)