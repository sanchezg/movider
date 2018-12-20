from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Currency, Provider, ServiceArea


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
        fields = '__all__'


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency data."""

    class Meta:
        model = Currency
        fields = '__all__'
