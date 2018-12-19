# movider
An API to serve providers data and functions

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
$ docker run --name=postgis -d -e POSTGRES_USER=pgadmin -e POSTGRES_PASS=secretpassword -e POSTGRES_DBNAME=gis -e ALLOW_IP_RANGE=0.0.0.0/0 -p 5432:5432 -v pg_data:/var/lib/postgresql --restart=always kartoza/postgis
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

