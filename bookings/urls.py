from django.urls import path

from . import views


urlpatterns = [
    path(
        "create/",
        views.booking_create,
        name="booking_create",
    ),
]