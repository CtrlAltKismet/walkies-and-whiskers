from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm
from .models import Pet


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

            return redirect("pet_list")
    else:
        form = PetForm()

    context = {
        "form": form,
    }

    return render(request, "pets/pet_form.html", context)


@login_required
def pet_list(request):
    """Display pet profiles belonging to the logged-in user."""

    pets = Pet.objects.filter(owner=request.user)

    context = {
        "pets": pets,
    }

    return render(request, "pets/pet_list.html", context)


@login_required
def pet_detail(request, pet_id):
    """Display a detailed pet profile belonging to the logged-in user."""
    
    pet = get_object_or_404(
        Pet,
        id=pet_id,
        owner=request.user,
    )
    
    context = {
        "pet": pet,
    }
    
    return render(
        request,
        "pets/pet_detail.html",
        context,
    )
    
    