import os
import random
import sys

sys.path.append('../')
os.environ['DJANGO_SETTINGS_MODULE'] = 'movider.settings'

import django  # noqa

from django.conf.global_settings import LANGUAGES  # noqa
from django.contrib.gis.geos import Polygon  # noqa

django.setup()

from providers.models import Currency, Provider, ServiceArea  # noqa

currencies_mocks = [
    # Basic currencies, more can be added then
    Currency(code='ARS', description='Argentine Pesos'),
    Currency(code='AUD', description='Australian Dollars'),
    Currency(code='BOB', description='Bolivian'),
    Currency(code='BRL', description='Brazilian Real'),
    Currency(code='CAD', description='Canadian Dollars'),
    Currency(code='CLP', description='Chilean Peso'),
    Currency(code='COP', description='Colombian Pesos'),
    Currency(code='CUP', description='Cubean Peso'),
    Currency(code='EUR', description='Euro'),
    Currency(code='GBP', description='Pound sterling'),
    Currency(code='JPY', description='Japanese Yen'),
    Currency(code='NZD', description='New Zealand Dollars'),
    Currency(code='PEN', description='Nuevo Sol'),
    Currency(code='QAR', description='Qatari Rial'),
    Currency(code='RUR', description='Russian Ruble'),
    Currency(code='USD', description='United States Dollars'),
    Currency(code='UYU', description='Peso Uruguayo'),
    Currency(code='VEF', description='Venezuelan Bolivar'),
    Currency(code='ZAR', description='Rand'),
    Currency(code='Other', description='Other'),
]
Currency.objects.bulk_create(currencies_mocks)

providers_mocks = [
    Provider(name='Fake provider 1', email='prov1@email.com', phone_number='123-456-71',
             language=random.choice(LANGUAGES)[0],
             currency=Currency.objects.get(id=random.randint(1, len(currencies_mocks)))),
    Provider(name='Fake provider 2', email='prov2@email.com', phone_number='123-456-72',
             language=random.choice(LANGUAGES)[0],
             currency=Currency.objects.get(id=random.randint(1, len(currencies_mocks)))),
    Provider(name='Fake provider 3', email='prov3@email.com', phone_number='123-456-73',
             language=random.choice(LANGUAGES)[0],
             currency=Currency.objects.get(id=random.randint(1, len(currencies_mocks)))),
    Provider(name='Fake provider 4', email='prov4@email.com', phone_number='123-456-74',
             language=random.choice(LANGUAGES)[0],
             currency=Currency.objects.get(id=random.randint(1, len(currencies_mocks)))),
    Provider(name='Fake provider 5', email='prov5@email.com', phone_number='123-456-75',
             language=random.choice(LANGUAGES)[0],
             currency=Currency.objects.get(id=random.randint(1, len(currencies_mocks)))),
]
Provider.objects.bulk_create(providers_mocks)


manhattan = (
    (40.7510527, -74.0072617), (40.8650854, -73.9310548), (40.8562003, -73.9233622), (40.8264163, -73.9332569),
    (40.7980769, -73.9254516), (40.7562156, -73.9606985), (40.7375309, -73.9746889), (40.710648, -73.9785916),
    (40.7100319, -73.992236), (40.7039667, -74.0146378), (40.7510527, -74.0072617)
)

ny = (
    (40.8324095, -74.0457782), (40.7881248, -73.9688256), (40.7121789, -74.0079644), (40.7189447, -74.1150811),
    (40.8324095, -74.0457782)
)

philadelphia = (
    (40.037694, -75.3029162), (39.9093001, -75.2727038), (39.9061398, -74.9225146), (40.0461049, -74.7700793),
    (40.1612143, -74.8908055), (40.298995, -75.1161486), (40.037694, -75.3029162)
)

washington = (
    (39.0061581, -77.129817), (38.8854669, -77.1339369), (38.8886737, -76.9348097), (38.9303495, -76.8098402),
    (39.0016684, -76.8966579), (39.0409425, -76.9641852), (39.0061581, -77.129817)
)

east_coast = (
    (41.4283447, -75.0331879), (39.1833375, -77.6808929), (38.5245665, -76.9228363), (39.2259037, -75.9120941),
    (39.4405017, -74.6781921), (40.1495538, -74.4145203), (40.6827534, -73.4951019), (41.419061, -73.6725998),
    (41.8705994, -73.9692307), (41.4283447, -75.0331879)
)

austin = (
    (30.1246025, -97.9412055), (30.3857406, -97.7670979), (30.3429171, -97.5731635), (30.1103478, -97.6116157),
    (30.1246025, -97.9412055)
)

san_antonio = (
    (29.3088171, -98.7322211), (29.2976086, -98.2964694), (29.5057838, -98.2442844), (29.5989651, -98.4667575),
    (29.522515, -98.7166965), (29.3095842, -98.733176), (29.3088171, -98.7322211)
)

texas = (
    (29.4461004, -99.1258192), (30.3603598, -98.3238173), (30.0105071, -95.0847602), (29.364654, -95.2010715),
    (29.4461004, -99.1258192)
)

central = (
    (34.0681606, -100.2856064), (32.3215194, -97.2753525), (34.340743, -95.7152939), (38.3563303, -96.4843369),
    (38.339098, -100.0439072), (34.0681606, -100.2856064)
)

kansas = (
    (39.2735272, -95.0329399), (38.7271037, -94.7912407), (38.9239603, -94.0221977), (39.4943049, -94.2419243),
    (39.2735272, -95.0329399)
)

service_area_mocks = [
    # Polygons are defined in this way to have some of them overlapped
    ServiceArea(name='SA1', price=random.random() * 100, polygon=Polygon(manhattan),
                provider=Provider.objects.get(id=1)),
    ServiceArea(name='SA2', price=random.random() * 100, polygon=Polygon(kansas),
                provider=Provider.objects.get(id=1)),
    ServiceArea(name='SA3', price=random.random() * 100, polygon=Polygon(ny),
                provider=Provider.objects.get(id=2)),
    ServiceArea(name='SA4', price=random.random() * 100, polygon=Polygon(central),
                provider=Provider.objects.get(id=2)),
    ServiceArea(name='SA5', price=random.random() * 100, polygon=Polygon(texas),
                provider=Provider.objects.get(id=3)),
    ServiceArea(name='SA6', price=random.random() * 100, polygon=Polygon(philadelphia),
                provider=Provider.objects.get(id=3)),
    ServiceArea(name='SA7', price=random.random() * 100, polygon=Polygon(san_antonio),
                provider=Provider.objects.get(id=4)),
    ServiceArea(name='SA8', price=random.random() * 100, polygon=Polygon(washington),
                provider=Provider.objects.get(id=4)),
    ServiceArea(name='SA9', price=random.random() * 100, polygon=Polygon(east_coast),
                provider=Provider.objects.get(id=5)),
    ServiceArea(name='SA10', price=random.random() * 100, polygon=Polygon(austin),
                provider=Provider.objects.get(id=5)),
]
ServiceArea.objects.bulk_create(service_area_mocks)

print("Succesfully created %d instances!" % (len(service_area_mocks) + len(providers_mocks) + len(currencies_mocks)))
