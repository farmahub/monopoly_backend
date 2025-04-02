from . import views

from django.urls import path


urlpatterns = [
    path("", views.PlayerApiView.as_view(), name="player_api_view"),
    path("property/", views.PlayerPropertyApiView.as_view(), name="player_property_api_view"),
]