from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
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
        else:
            return Response(
                {"error": "invalide serializer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
