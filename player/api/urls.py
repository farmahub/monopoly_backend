from . import views

from django.urls import path


urlpatterns = [
    path("", views.PlayerApiView.as_view(), name="player_api_view"),
    path("property/", views.PlayerPropertyApiView.as_view(), name="player_property_api_view"),
    path("property/buy/", views.PlayerBuyPropertyApiView.as_view(), name="player_buy_property_api_view"),
]