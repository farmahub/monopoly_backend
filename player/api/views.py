from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from player.models import Player
from player.serializers import PlayerSerializer
from property.models import Property
from property.serializers import PropertySerializer
from player.serializers import PlayerSerializer


class PlayerApiView(APIView):
    def get(self, request, format=None):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PlayerPropertyApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            properties = Property.objects.filter(owner=user.id)
            serializer = PropertySerializer(properties, many=True)
            return Response(
                {
                    "id": user.id,
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"error": "user is not authenticated"})
