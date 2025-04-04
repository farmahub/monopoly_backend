from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from wallet.models import Wallet
from wallet.serializers import WalletSerializer
from property.models import Property
from property.serializers import PropertySerializer


class WalletApiView(APIView):
    def get(self, request, format=None):
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class WalletPropertyApiView(APIView):
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
