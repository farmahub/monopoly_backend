from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from room.models import Ticket
from .serializers import UserSerializer


class RegisterView(APIView):
    permission_classes = []
    template_name = "register_form"

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
    