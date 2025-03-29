from django.urls import path

from . import views


urlpatterns = [
    path("", views.PropertyApiView.as_view(), name="property_api_view"),
    path("detail/<int:pk>/", views.PropertyDetailApiView.as_view(), name="property_detail_api_view"),
]
