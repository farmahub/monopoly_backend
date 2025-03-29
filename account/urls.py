from django.urls import path

from . import views


urlpatterns = [
    path("", views.RegisterUserView.as_view(), name="register_user_view"),
]
