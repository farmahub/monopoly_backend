from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import redirect

from ..models import Room, Ticket
from ..serializers import RoomSerializer, TicketSerializer
from account.serializers import UserSerializer


class CreateRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = {
            "name": request.data.get("name"),
            "admin": request.user.id,
        }
        serializer = RoomSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "room is created"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateTicketView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "ticket is created"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendTicketView(APIView):
    permission_classes = []
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            recipient_email = request.data.get("email")

            if not recipient_email:
                return Response({"error": "recipient email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            ticket.send_ticket_email(recipient_email)

            return Response({"message": f"ticket is sent to {recipient_email} successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class UseTicketView(APIView):
    permission_classes = []
    def get(self, request, ticket_id):
        try:
            if not request.user.is_authenticated:
                return redirect(f"/account/?ticket_id={ticket_id}")
            
            user = request.user
            ticket = Ticket.objects.get(id=ticket_id)
            room = ticket.room

            if ticket.is_expired:
                return Response({"error": "the ticket is expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            if ticket.is_used:
                return Response({"error": "the ticket is expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            room.player.add(user)
            room.save()
            ticket.is_used = True
            ticket.issued_to = user
            ticket.save()
            
            return Response({"message": "user is joined to the room"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        