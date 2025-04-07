from django.urls import path

from . import views


urlpatterns = [
    path("create-room/", views.CreateRoomView.as_view(), name="create_room"),
    path("create-ticket/", views.CreateTicketView.as_view(), name="create_ticket"),
    path("send-ticket/<str:ticket_id>/", views.SendTicketView.as_view(), name="send_ticket"),
    path("use-ticket/<str:ticket_id>/", views.UseTicketView.as_view(), name="use_ticket"),
]