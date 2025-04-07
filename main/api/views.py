from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly

from django.http import JsonResponse

from account.models import User
from account.serializers import UserSerializer


class TestView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        print(f"Headers: {request.headers}")  # Log all headers

        if request.user.is_authenticated:
            return Response({
                "message": "IsAuthenticated",
                "user": str(request.user),
            })
        return Response({"message": "ReadOnly"})