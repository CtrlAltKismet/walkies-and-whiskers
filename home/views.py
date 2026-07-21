from django.shortcuts import render


def home(request):
    """Display the homepage."""
    return render(request, "home/index.html")

def about(request):
    """Display the about page."""
    return render(request, "home/about.html")