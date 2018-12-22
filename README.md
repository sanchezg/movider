# movider
An API to serve providers data and functions.

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
- Project hasn't authentication, it can be added with a bit more development time (some options include json-web-token).
- Coding style was mostly written following pep8 and pycodestyle suggestions, but some issues can be found.
- Due to serializer issues, some ServiceArea endpoint unit tests are broken, they were marked with skip to not show
errors on development stage.
- The application has been developed using Python 3.7.0. There aren't big changes with any version up to 3.5+.
But I can't ensure that the other used packages will work well with those Python versions.
- The application was deployed using a very basic approach (download in the server, and install). CI/CD can be helpful
here.

**Additional notes**

- There's an extra `utils/populate_db.py` script that will load 5 Providers with 2 ServiceAreas each one of them.
Follow it to look how to load more data programatically.
- You will need to create a `local_settings.py` in the same package as `settings.py`, with at least the following
information:

```
DEBUG = False  # Production ready app
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': '<DB_NAME>',
        'USER': '<DB_USER>',
        'PASSWORD': '<DB_PASSWORD>',
        'HOST': '<DB_SERVER>',
        'PORT': '<DB_PORT>'
    }
}
```

## Deployment/Installation notes

The application is deployed on a public AWS EC2 instance with Ubuntu 18.04.
You can access to it using the following URL: <PRIVATE_ADDRESS>.

**Steps**

Following steps are for an equivalent system to the one used in the deploy.

1. Make sure you have all necessary packages and libraries to build and run your application:

```
$ sudo apt-get install build-essential libsqlite3-dev sqlite3 \
    bzip2 libbz2-dev zlib1g-dev libssl-dev openssl libgdbm-dev \
    libgdbm-compat-dev liblzma-dev libreadline-dev libncursesw5-dev libffi-dev uuid-dev \
    apt-transport-https ca-certificates curl software-properties-common \
    git
```

2. Install Python and dependencies

- Install `pyenv` and Python 3.7.0: https://github.com/pyenv/pyenv#installation
- Install `Pipenv`:

```
$ pip install -U pip
$ pip install pipenv
```

- Install dependencies:

```
$ pipenv install
```

3. Install GEOS, PROJ.4 and GDAL for the proper working with PostGIS:

On Ubuntu:

```
$ sudo apt-get install libgeos-dev binutils libproj-dev gdal-bin libgdal-dev python3-gdal
```

On macOS:

```
$ brew install geos
$ brew install proj
$ brew install gdal2
```

3. Install Docker (for the DB) using your preferred method.

4. Pull a PostGIS container:

```
$ docker volume create pg_data
$ docker run --name=postgis -d -e POSTGRES_USER=<DB_USER> \
                               -e POSTGRES_PASS=<DB_PASSWORD> \
                               -e POSTGRES_DBNAME=<DB_NAME> \
                               -e ALLOW_IP_RANGE=0.0.0.0/0 \
                               -p 5432:5432 -v pg_data:/var/lib/postgresql \
                               --restart=always kartoza/postgis
```

Notice that you must create a persistant volume to keep database data.

5. Migrate the Django App:

```
movider/ $ pipenv run python manage.py migrate
```

6. Create static files:

```
movider/ $ pipenv run python manage.py collectstatic
```

7. [OPTIONAL] Load database with pre-computed data:

```
movider/utils/ $ pipenv run python populate_db.py
```

You will see the following message:

```
Succesfully created 35 instances!
```

## Run

Run the local development server with:

```
movider/ $ pipenv python manage.py runserver
```

## Usage

**Create a new currency**

```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d '{"code": "USD", "description": "US Dollars"}' \
 'http://<SERVER_ADDRESS>/api/v0/currencies/'
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
  "currency": "http://<SERVER_ADDRESS>/api/v0/currencies/1/",
  "service_areas": []
}' \
 'http://<SERVER_ADDRESS>/api/v0/providers/'
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
 'http://<SERVER_ADDRESS>/api/v0/serviceareas/'
```

**Retrieve service areas for a current geo point (pair of 'latitude, longitude')**

```
curl -i -X GET 'http://<SERVER_ADDRESS>/api/v0/serviceareas_by_location/?latitude=1.0&longitude=1.0'
```
