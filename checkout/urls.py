from django.urls import include, path

from . import views


urlpatterns = [
    path(
        "<int:booking_id>/",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path(
        "success/",
        views.payment_success,
        name="payment_success",
    ),
    path(
        "cancel/<int:booking_id>/",
        views.payment_cancel,
        name="payment_cancel",
    ),
]
