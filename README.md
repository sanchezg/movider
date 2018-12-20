# movider
An API to serve providers data and functions

## Introduction

This is a demo project using Django, rest-framework, Postgres and PostGIS which main purpose is to query
what are the _Providers_ that serves a _ServiceArea_; and, given a location by it `latitude` and `longitude` geo
coordinates, discover the _ServiceAreas_ and corresponding _Providers_ that includes that location.

### Development notes

Refer to **Installation** section to install locally the project, and run the tests:

```
movider/ $ python manage.py test
```

**Technical debt**

- The project has _some_ unit tests, more can be added as the functionality grows.
- Some models and fields can be improved using validators (for example `phone_number`, `email`, etc).
- Project hasn't authentication, it can be added with more time (some options include json-web-token).
- Coding style was mostly written folowing pep8 and pycodestyle suggestions, but some issues can be found.
- Due to serializer issues, some ServiceArea endpoint tests are broken, they were marked with skip to not show errors
on development stage.

## Installation

1. Clone or download this repo

2. Install `pyenv` and `Pipenv`

3. Install GEOS, PROJ.4 and GDAL for the proper working with PostGIS:

On Ubuntu:

```
$ sudo apt-get install libgeos-dev
$ sudo apt-get install binutils libproj-dev
$ sudo apt-get install gdal-bin libgdal-dev
$ sudo apt-get install python3-gdal
```

On macOS:

```
$ brew install geos
$ brew install proj
$ brew install gdal2
```

4. Pull a PostGIS container:

```
$ docker volume create pg_data
$ docker run --name=postgis -d -e POSTGRES_USER=pgadmin \
                               -e POSTGRES_PASS=secretpassword \
                               -e POSTGRES_DBNAME=gis \
                               -e ALLOW_IP_RANGE=0.0.0.0/0 \
                               -p 5432:5432 -v pg_data:/var/lib/postgresql \
                               --restart=always kartoza/postgis
```

Notice that you must create a persistant volume to keep database data.


5. Migrate the Django App:

```
movider/ $ python manage.py migrate
```

6. [OPTIONAL] Load database with pre-computed data:

```
movider/utils/ $ python populate_db.py
```

You will see the following message:

```
Succesfully created 35 instances!
```

## Run

Run the local development server with:

```
movider/ $ python manage.py runserver
```

## Usage

**Create a new currency**

```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d '{"code": "USD", "description": "US Dollars"}' \
 'http://<server_address>/api/v0/currencies/'
```

**Create a new provider**

```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "name": "New Provider Name",
  "email": "info@newprovider.com",
  "phone_number": "+1 234 5678",
  "language": "en",
  "currency": "http://<server_address>/api/v0/currencies/1/",
  "service_areas": []
}' \
 'http://<server_address>/api/v0/providers/'
```

**Create a new service area**

```
curl \
 -X POST \
 -H 'Accept: application/json' \
 -d name="Service Area Name" \
 -d provider=1 \
 -d price=10.27 \
 -d polygon='{"coordinates": [
            [ [10.0, 20.0], [15.0, 20.0], [15.0, 35.0],
              [10.0, 35.0], [10.0, 20.0] ]
        ], "type": "Polygon"}'  \
 'http://<server_address>/api/v0/serviceareas/'
```

**Retrieve service areas for a current geo point (pair of 'latitude, longitude')**

```
curl -i -X GET 'http://<server_address>/api/v0/serviceareas_by_location/?latitude=1.0&longitude=1.0'
```
