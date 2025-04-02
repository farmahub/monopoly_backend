from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),  # registration_handling
    path("api/account/", include("account.api.urls")),  # token_handling
    path("api/property/", include("property.api.urls")),
    path("api/player/", include("player.api.urls")),
    path("actions/player/", include("player.actions.urls")),
]
