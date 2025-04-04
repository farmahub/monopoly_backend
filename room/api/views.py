from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import Room, Ticket
from ..serializers import RoomSerializer, TicketSerializer


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
