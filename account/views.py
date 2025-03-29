from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


from .models import User
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


class RegisterUserView(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": "User created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "invalide serializer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
