import factory
import random

from django.conf.global_settings import LANGUAGES
from django.contrib.gis.geos import Polygon
from providers import models


class CurrencyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Currency
        django_get_or_create = ('code', 'description',)
    code = factory.Sequence(lambda n: "code_%d" % n)
    description = factory.Sequence(lambda n: "currency_%d" % n)


class ProviderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Provider
        django_get_or_create = ('name',)
    name = factory.Sequence(lambda n: "provider_%d" % n)
    email = factory.Sequence(lambda n: "provider_%d@fake.com" % n)
    phone_number = '1 800 123 4578'
    language = random.choice(LANGUAGES)[0]
    currency = factory.SubFactory(CurrencyFactory)


class ServiceAreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ServiceArea
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: "service_area_%d" % n)
    provider = factory.SubFactory(ProviderFactory)
    polygon = Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)))
    price = 15.
