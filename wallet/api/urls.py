from . import views

from django.urls import path


urlpatterns = [
    path("", views.WalletApiView.as_view(), name="wallet_api_view"),
    path("property/", views.WalletPropertyApiView.as_view(), name="wallet_property_api_view"),
]