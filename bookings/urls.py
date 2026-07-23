from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.booking_list,
        name="booking_list",
    ),
    path(
        "create/",
        views.booking_create,
        name="booking_create",
    ),
    path(
        "<int:booking_id>/",
        views.booking_detail,
        name="booking_detail",
    ),
    path(
        "<int:booking_id>/cancel/",
        views.booking_cancel,
        name="booking_cancel",
    ),
]