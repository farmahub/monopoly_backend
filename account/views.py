from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from room.models import Ticket
from .serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User(email=serializer.validated_data["email"])
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response(
                {"success": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        ticket_id = request.GET.get("ticket_id")
        ticket = Ticket.objects.get(id=ticket_id)
        room = ticket.room
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            if ticket.is_used:
                return Response(
                    {"error": "Ticket is used"}, status=status.HTTP_400_BAD_REQUEST
                )

            if ticket.is_expired:
                return Response(
                    {"error": "Ticket is expired"}, status=status.HTTP_400_BAD_REQUEST
                )

            user = User(email=serializer.validated_data["email"])
            user.set_password(serializer.validated_data["password"])
            user.save()
            room.player.add(user)
            room.save()
            ticket.is_used = True
            ticket.issued_to = user
            ticket.save()

            return Response(
                {"success": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
