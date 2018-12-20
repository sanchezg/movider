from django.contrib.gis.geos import Point
from rest_framework import filters, viewsets
from rest_framework.response import Response

from .models import Currency, Provider, ServiceArea
from .serializers import (CoordinateSerializer, CurrencySerializer, ProviderSerializer,
                          ServiceAreaSerializer)


class ProviderIsInPolygonFilterBackend(filters.BaseFilterBackend):
    """Filter Providers that have service areas in the provided geo point."""

    def filter_queryset(self, request, queryset, view):
        coords = CoordinateSerializer(data=request.query_params)
        if coords.is_valid():
            lat, lng = coords.validated_data.values()
            geo_point = Point(lat, lng)
            provider_ids = ServiceArea.objects.filter(polygon__contains=geo_point).values('provider_id')
            queryset = queryset.filter(id__in=provider_ids)
        return queryset


class ProviderViewSet(viewsets.ModelViewSet):
    """Viewset for retrieve, create, update and delete Provider objects."""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    filter_backends = (ProviderIsInPolygonFilterBackend,)


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """ViewSet for retrieve, create, update and delete ServiceArea objects."""
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """ViewSet for retrieve, create, update and delete Currency objects."""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
