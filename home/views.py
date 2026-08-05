from django.shortcuts import render


def home(request):
    """Display the homepage."""
    return render(request, "home/index.html")


def about(request):
    """Display the about page."""
    return render(request, "home/about.html")


def custom_404(request, exception):
    """Display the custom page-not-found response."""

    return render(
        request,
        "404.html",
        status=404,
    )
