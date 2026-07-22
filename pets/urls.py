from django.urls import path

from . import views


urlpatterns = [
    path(
        "add/",
        views.pet_create,
        name="pet_create",
    ),
]