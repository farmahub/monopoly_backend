from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path("", views.CustomTokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view, name="token_refresh"),
]
