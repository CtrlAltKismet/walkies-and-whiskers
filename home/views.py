from django.shortcuts import render


def home(request):
    """Display the homepage."""
    return render(request, "home/index.html")