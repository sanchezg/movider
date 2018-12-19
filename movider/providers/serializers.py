from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from .models import Provider, ServiceArea


class ProviderSerializer(serializers.ModelSerializer):
    """Serializer for Providers."""

    class Meta:
        model = Provider
        fields = '__all__'


class ServiceAreaSerializer(GeoFeatureModelSerializer):
    """Serializer for Service Areas."""

    class Meta:
        model = ServiceArea
        geo_field = "polygon"
        fields = '__all__'
