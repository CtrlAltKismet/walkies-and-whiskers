from django.urls import include, path

from . import views


urlpatterns = [
    path(
        "<int:booking_id>/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path(
        "checkout/",
        include("checkout.urls"),
    ),
]