from django.urls import path

from . import views

urlpatterns = [
    path("jail-action/", views.WalletJailActionView.as_view(), name="jail_action"),
]