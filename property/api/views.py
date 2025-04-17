from ..serializers import PropertySerializer
from ..models import Property

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from django.http import Http404


class PropertiesApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PropertyDetailApiView(APIView):
    def get_bject(self, pk):
        try:
            return Property.objects.get(pk=pk)

        except Property.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        property = self.get_bject(pk)
        serializer = PropertySerializer(property)

        return Response(serializer.data, status=status.HTTP_200_OK)