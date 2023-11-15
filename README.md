# Indigenous Garden Map & Educational tool

The Indigenous Gardens grows on the traditional and unceded territories of the kʷikʷəƛ̓əm (Kwikwetlem), Sḵwx̱wú7mesh Úxwumixw (Squamish), Səl̓ilw̓ətaʔɬ (Tsleil-Waututh), and Xʷməθkʷəy̓əm (Musqueam), who are the original caretakers of these lands and have been since time immemorial. We have a responsibility to ensure that their traditional ways of knowing, being, and doing are woven within this space and to give garden visitors an opportunity to reflect on their relationships with the natural world. Indigenous knowledge systems carry rich knowledge of plants and their traditional uses that result from being in relationship with these lands for thousands of years. This project will allow us to learn, preserve and share traditional plant knowledge with garden visitors in a unique and interactive way. The project will be used for general garden navigation as well as for learning and reflection.


## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Initialize the Application

    docker compose up -d --build

Indigenous Garden Map will be available at `http://localhost:8080/`
Indigenous Garden Admin will be available at `http://localhost:8080/admin/`

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
    docker logs -f indigenous_garden_db
    docker logs -f indigenous_garden_mail

### Accessing the Application

    http://localhost:8080/

### Accessing the Database

Command line:

    docker exec -it indigenous_garden_db mysql -u indigenous_garden -ppassword indigenous_garden

Through a database management tool:
- Host:`127.0.0.1`
- Port: `13306`
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

First setup an image to build the yarn deps in

    docker build -t indigenous_garden_yarn_helper --target indigenous-garden-prod-assets .

Then run the following as needed

    # add new package
    docker run -it --rm -v $(pwd):/app indigenous_garden_yarn_helper yarn add [package]

    # update a package
    docker run -it --rm -v $(pwd):/app indigenous_garden_yarn_helper yarn upgrade [package]

    # update all packages
    docker run -it --rm -v $(pwd):/app indigenous_garden_yarn_helper yarn upgrade

Note: If you are having problems starting/building the application due to javascript dependencies issues you can also run a standalone node container to help resolve them

    docker run -it --rm -v $(pwd):/app -w /app node:19.5 bash

    [check Dockerfile for the 'apt-get update' code piece of indigenous-garden-prod-assets]

    yarn ...

After you update a dependency make sure to rebuild the images

    docker compose down
    docker compose up -d

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

## Tests
