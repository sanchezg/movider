from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.contrib.gis.db import models


class Currency(models.Model):
    """Basic model to represent a currency."""

    code = models.CharField("Code", max_length=settings.MAX_CHAR_LENGTH)
    description = models.CharField("Description", max_length=settings.MAX_CHAR_LENGTH)

    def __str__(self):
        return self.code


class Provider(models.Model):
    """Represent a Provider."""

    name = models.CharField("Name", max_length=settings.MAX_CHAR_LENGTH)
    email = models.EmailField("e-mail", unique=True, max_length=settings.MAX_CHAR_LENGTH)
    phone_number = models.CharField("Phone number", max_length=settings.MAX_CHAR_LENGTH)
    language = models.CharField("Language", max_length=50, choices=LANGUAGES, default='en')
    currency = models.ForeignKey("Currency", related_name='providers', on_delete=models.SET_DEFAULT, default='')

    def __str__(self):
        return self.name


class ServiceArea(models.Model):
    """Represent a Service Area bounded by a polygon of GEO coordinates."""

    provider = models.ForeignKey('Provider', on_delete=models.CASCADE, related_name='service_areas')
    name = models.CharField("Name", max_length=settings.MAX_CHAR_LENGTH)
    price = models.DecimalField("Price", max_digits=100, decimal_places=2)
    polygon = models.PolygonField("Polygon")

    def __str__(self):
        return "{} - {}".format(self.provider.name, self.name)
