from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),  # registration_handling
    path("api/account/", include("account.api.urls")),  # token_handling
    path("api/property/", include("property.api.urls")),
    path("api/wallet/", include("wallet.api.urls")),
    path("api/room/", include("room.api.urls")),
    path("actions/wallet/", include("wallet.actions.urls")),
]
