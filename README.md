[![Docker Image Latest Badge](https://ghcr-badge.egpl.dev/sfu-dhil/indigenous-garden/latest_tag?trim=major&label=latest)](https://github.com/sfu-dhil/indigenous-garden/pkgs/container/indigenous-garden)
[![Docker Image Size badge](https://ghcr-badge.egpl.dev/sfu-dhil/indigenous-garden/size)](https://github.com/sfu-dhil/indigenous-garden/pkgs/container/indigenous-garden)

# Indigenous Garden Map & Educational tool

The Indigenous Gardens grows on the traditional and unceded territories of the kʷikʷəƛ̓əm (Kwikwetlem), Sḵwx̱wú7mesh Úxwumixw (Squamish), Səl̓ilw̓ətaʔɬ (Tsleil-Waututh), and Xʷməθkʷəy̓əm (Musqueam), who are the original caretakers of these lands and have been since time immemorial. We have a responsibility to ensure that their traditional ways of knowing, being, and doing are woven within this space and to give garden visitors an opportunity to reflect on their relationships with the natural world. Indigenous knowledge systems carry rich knowledge of plants and their traditional uses that result from being in relationship with these lands for thousands of years. This project will allow us to learn, preserve and share traditional plant knowledge with garden visitors in a unique and interactive way. The project will be used for general garden navigation as well as for learning and reflection.


## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Initialize the Application

    docker compose up -d --build

Indigenous Garden Map will be available at `http://localhost:8080/`
Indigenous Garden Admin will be available at `http://localhost:8080/admin/`

### Install/Switch the admin theme

    # Bootstrap
    docker exec -it indigenous_garden_app python manage.py loaddata admin_interface_theme_bootstrap.json

    # Django
    docker exec -it indigenous_garden_app python manage.py loaddata  admin_interface_theme_django.json

    # Foundation
    docker exec -it indigenous_garden_app python manage.py loaddata  admin_interface_theme_foundation.json

    # U.S. Web Design Standards
    docker exec -it indigenous_garden_app python manage.py loaddata  admin_interface_theme_uswds.json

### Create your superuser

    docker exec -it indigenous_garden_app python manage.py createsuperuser

Enter `username`, `email`, and `password` as prompted

example:

    docker exec -it indigenous_garden_app python manage.py createsuperuser --username="admin" --email="dhil@sfu.ca"

## General Usage

### Starting the Application

    docker compose up -d

### Stopping the Application

    docker compose down

### Rebuilding the Application (after upstream or js/python package changes)

    docker compose up -d --build

### Viewing logs (each container)

    docker logs -f indigenous_garden_app
    docker logs -f indigenous_garden_vite
    docker logs -f indigenous_garden_nginx
    docker logs -f indigenous_garden_db
    docker logs -f indigenous_garden_mail

### Accessing the Application

    http://localhost:8080/

### Accessing the Database

Command line:

    PGPASSWORD=password docker exec -it indigenous_garden_db psql --username=indigenous_garden indigenous_garden

Through a database management tool:
- Host:`127.0.0.1`
- Port: `15432`
- Username: `indigenous_garden`
- Password: `password`

### Accessing Mailhog (catches emails sent by the app)

    http://localhost:8025/

### Database Migrations

Migrate up to latest

    docker exec -it indigenous_garden_app python manage.py migrate

Create new migrations

    docker exec -it indigenous_garden_app python manage.py makemigrations

## Updating Application Dependencies

### Yarn (javascript)

    # add new package
    docker exec -it indigenous_garden_vite yarn add [package]

    # update a package
    docker exec -it indigenous_garden_vite yarn upgrade [package]

    # update all packages
    docker exec -it indigenous_garden_vite yarn upgrade

After you update a dependency make sure to rebuild the images

    docker compose down
    docker compose up -d --build

### Pip (python)

Manage python dependencies in `requirements.txt`
>All packages should be locked to a specific version number if possible (Ex `Django==4.2.7`)
>Some special packages cannot be locked and should be noted as such (Ex `psycopg[binary]`)

After making changes, you need to run pip or rebuild the image

    docker exec -it indigenous_garden_app pip install -r requirements.txt
    # or
    docker compose up -d --build

#### Update a package

Edit version number in `requirements.txt` with new locked version number
>Ex `pip==24.0.0`

    docker exec -it indigenous_garden_app pip install -r requirements.txt
    # or
    docker compose up -d --build

## Upgrade Postgres Docker version

First turn off everything

    docker compose down

Then backup the postgres data folder

    cp -R .data/postgres .data/postgres-backup

Setup the new version dir

    sudo mkdir -p .data/postgres/<NEW POSTGRES VERSION>/docker
    sudo chown 999:999 -R .data/postgres/<NEW POSTGRES VERSION>
    # example:
    sudo mkdir -p .data/postgres/18/docker
    sudo chown 999:999 -R .data/postgres/18


Using `https://github.com/tianon/docker-postgres-upgrade` to upgrade the postgres version

    docker run --rm \
        --volume .data/postgres:/var/lib/postgresql \
        --env PGDATAOLD=/var/lib/postgresql/<OLD POSTGRES VERSION>/docker \
        --env PGDATANEW=/var/lib/postgresql/<NEW POSTGRES VERSION>/docker \
        --env POSTGRES_USER=indigenous_garden \
        --env POSTGRES_PASSWORD=password \
        tianon/postgres-upgrade:<OLD POSTGRES VERSION>-to-<NEW POSTGRES VERSION> \
        --link

example:

    docker run --rm \
        --volume .data/postgres:/var/lib/postgresql \
        --env PGDATAOLD=/var/lib/postgresql/17/docker \
        --env PGDATANEW=/var/lib/postgresql/18/docker \
        --env POSTGRES_USER=indigenous_garden \
        --env POSTGRES_PASSWORD=password \
        tianon/postgres-upgrade:17-to-18 \
        --link

## Creating map tiles of static image

install `gdal` (via homebrew): `brew install gdal`

Generate the files from some import source:

```shell
gdal2tiles --xyz --profile=raster --zoom=1-6 --tiledriver=WEBP --tilesize=128 .data/static-assets/images/garden.png .data/static-assets/images/garden
```

## Create multi resolution tiles for panorama image

See [pannellum docs](https://github.com/mpetroff/pannellum/tree/master/utils/multires) for using docker.

First download pannellum master locally

```shell
cd <pannellum folder>/utils/multires/
docker build -t generate-panorama .
```

Then in this project

    docker run --rm -it \
        -v $PWD/.data/static-assets/images/:/data \
        generate-panorama --output /data/panorama_location_1 /data/panorama_location_1.png

    docker run --rm -it \
        -v $PWD/.data/static-assets/images/:/data \
        generate-panorama --output /data/panorama_location_2 /data/panorama_location_2.png

    docker run --rm -it \
        -v $PWD/.data/static-assets/images/:/data \
        generate-panorama --output /data/panorama_location_3 /data/panorama_location_3.png