from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ServiceArea
from .serializers import CoordinateSerializer, ServiceAreaSerializer


class ServiceAreasList(APIView):
    """List Service Areas that sorround a given geo point addressed by `latitude` and `longitude`."""

    def get(self, request):
        """GET method returns a list of the ServiceArea that match the given point."""

        coords = CoordinateSerializer(data=request.query_params)
        if not coords.is_valid():
            return Response(data=coords.errors, status=status.HTTP_400_BAD_REQUEST)

        lat, lng = coords.validated_data.values()
        queryset = ServiceArea.objects.filter(polygon__contains=Point(lat, lng))
        if queryset.exists():
            service_areas = [ServiceAreaSerializer(instance=sa).data for sa in queryset]
            return Response(service_areas)
        else:
            return Response(
                data={'Error': "No providers were found for the given point."},
                status=status.HTTP_404_NOT_FOUND)
