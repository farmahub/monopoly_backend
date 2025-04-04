from django.urls import path

from . import views


urlpatterns = [
    path("create-room/", views.CreateRoomView.as_view(), name="create_room"),
    path("create-ticket/", views.CreateTicketView.as_view(), name="create_ticket"),
]