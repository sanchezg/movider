from rest_framework import viewsets
from .models import Provider, ServiceArea
from .serializers import ProviderSerializer, ServiceAreaSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    """Viewset for retrieving / creating Provider model objects."""
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    """ViewSet for retrieving / creating ServiceArea model objects."""
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer
