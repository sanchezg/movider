from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Currency, Provider, ServiceArea


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency data."""

    class Meta:
        model = Currency
        fields = ('code', 'description')


class ProviderSerializer(serializers.ModelSerializer):
    """Serializer for Providers."""

    class Meta:
        model = Provider
        fields = ('name', 'email', 'phone_number', 'language', 'currency')


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    """Serializer for Service Areas."""

    class Meta:
        model = ServiceArea
        geo_field = "polygon"
        fields = ('name', 'price', 'provider', 'polygon')


class CoordinateSerializer(serializers.Serializer):
    """Validate latitude and longitude values from request."""

    latitude = serializers.FloatField(min_value=-90.0, max_value=90.0)
    longitude = serializers.FloatField(min_value=-180.0, max_value=180.0)
