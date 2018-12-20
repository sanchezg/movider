from unittest import skip

from django.contrib.gis.geos import Polygon
from django.core.serializers import serialize
from django.urls import reverse

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient, APITestCase

from providers.models import Currency, Provider, ServiceArea

from .factories import CurrencyFactory, ProviderFactory, ServiceAreaFactory


class CurrencyTests(APITestCase):
    def setUp(self):
        self.currency = CurrencyFactory(code='TST', description='Test')
        self.client = APIClient()

    def test_create_currency(self):
        url = reverse('currency-list')
        data = {'code': 'XYZ', 'description': 'Fake Desc'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.filter(code='XYZ').count(), 1)

    def test_retrieve_currency(self):
        url = reverse('currency-detail', args=[self.currency.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('code'), self.currency.code)
        self.assertEqual(response.data.get('description'), self.currency.description)

    def test_update_currency(self):
        url = reverse('currency-detail', args=[self.currency.id])
        data = {'code': 'TZT', 'description': 'Tezt'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Currency.objects.filter(code='TZT').count(), 1)

    def test_destroy_currency(self):
        url = reverse('currency-detail', args=[self.currency.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Currency.objects.count(), 0)


class ProviderTests(APITestCase):
    def setUp(self):
        self.provider = ProviderFactory()
        self.currency = CurrencyFactory()
        self.client = APIClient()

    def test_create_provider(self):
        url = reverse('provider-list')
        data = {
            'name': 'fake provider',
            'email': 'fake@fake.com',
            'phone_number': '0303456',
            'language': 'en',
            'currency': self.currency.id,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.filter(name='fake provider').count(), 1)

    def test_retrieve_provider(self):
        url = reverse('provider-detail', args=[self.provider.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.provider.name)

    def test_update_provider(self):
        url = reverse('provider-detail', args=[self.provider.id])
        data = {
            'name': 'other new fake provider',
            'email': 'fake@fake.com',
            'phone_number': '0303456',
            'language': 'en',
            'currency': self.currency.id,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.filter(phone_number='0303456').count(), 1)

    def test_destroy_provider(self):
        url = reverse('provider-detail', args=[self.provider.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Provider.objects.count(), 0)


class ServiceAreaTests(APITestCase):
    def setUp(self):
        self.service_area = ServiceAreaFactory()
        self.provider = ProviderFactory()
        self.currency = CurrencyFactory()
        self.client = APIClient()

    @skip("Not working")
    def test_create_servicearea(self):
        url = reverse('servicearea-list')
        data = serialize('geojson', [ServiceAreaFactory(name='fake SA')], geometry_field='polygon',
                         fields=('name', 'price', 'provider',))  # This isn't working
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceArea.objects.filter(name='fake SA').count(), 1)

    @skip("Not working")
    def test_retrieve_servicearea(self):  # This isn't working
        url = reverse('servicearea-detail', args=[self.service_area.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.service_area.name)

    @skip("Not working")
    def test_update_servicearea(self):  # This isn't working
        url = reverse('servicearea-detail', args=[self.service_area.id])
        data = {
            'name': 'fake SA 225',
            'provider': self.provider.id,
            'polygon': Polygon(((0, 0), (0, 2), (2, 2), (2, 0), (0, 0))),
            'price': 25.,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ServiceArea.objects.filter(name='fake SA 225').count(), 1)

    def test_destroy_provider(self):
        url = reverse('servicearea-detail', args=[self.service_area.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceArea.objects.count(), 0)


class ServiceAreasListTests(APITestCase):
    def setUp(self):
        self.service_area = ServiceAreaFactory(name='Test Area')
        self.url = reverse("servicesareas_by_location")

    def test_latitude_required(self):
        data = {'longitude': .1}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = {'latitude': [ErrorDetail(string='This field is required.', code='required')]}
        self.assertEqual(response.data, error_message)

    def test_longitude_required(self):
        data = {'latitude': .1}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_message = {'longitude': [ErrorDetail(string='This field is required.', code='required')]}
        self.assertEqual(response.data, error_message)

    def test_invalid_latitude_values(self):
        INVALID_LATITUDES = [
            {'value': -90.1,
             'error_message': 'Ensure this value is greater than or equal to -90.0.', 'code': 'min_value'},
            {'value': 90.1,
             'error_message': 'Ensure this value is less than or equal to 90.0.', 'code': 'max_value'},
        ]
        for lat in INVALID_LATITUDES:
            data = {'latitude': lat['value'], 'longitude': 0.}
            response = self.client.get(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_message = {
                'latitude': [ErrorDetail(string=lat['error_message'], code=lat['code'])]
            }
            self.assertEqual(response.data, error_message)

    def test_invalid_longitude_values(self):
        INVALID_LONGITUDES = [
            {'value': -180.1,
             'error_message': 'Ensure this value is greater than or equal to -180.0.', 'code': 'min_value'},
            {'value': 180.1,
             'error_message': 'Ensure this value is less than or equal to 180.0.', 'code': 'max_value'},
        ]
        for lng in INVALID_LONGITUDES:
            data = {'latitude': 0., 'longitude': lng['value']}
            response = self.client.get(self.url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            error_message = {
                'longitude': [ErrorDetail(string=lng['error_message'], code=lng['code'])]
            }
            self.assertEqual(response.data, error_message)

    def test_valid_coordinates_within_a_service_area(self):
        """Validate that the API answer with the object when a ServiceArea is found for the required location."""
        data = {'latitude': .5, 'longitude': .5}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.service_area.id)

    def test_valid_coordinates_without_a_service_area(self):
        """Validate that the API answer with 404 when a ServiceArea isn't found for the required location."""
        data = {'latitude': 5., 'longitude': 5.}
        response = self.client.get(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
