from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_places),
    path("create/", views.creation),
    path("/<str:place_id>/", views.get_place),
]
