from django.contrib.gis.geos import Point
from rest_framework import filters, viewsets
from rest_framework.response import Response

from .models import Currency, Provider, ServiceArea
from .serializers import CurrencySerializer, ProviderSerializer, ServiceAreaSerializer


class ProviderIsInPolygonFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        lat = request.query_params.get('latitude')
        lng = request.query_params.get('longitude')
        if lat is not None and lng is not None:
            geo_point = Point(float(lat), float(lng))
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
