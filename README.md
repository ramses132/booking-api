# booking-api

[![Build Status](https://travis-ci.com/ramses132/booking-api.svg?branch=master)](https://travis-ci.com/ramses132/booking-api)
[![Pyup](https://pyup.io/repos/github/ramses132/booking-api/shield.svg)](https://pyup.io/account/repos/github/ramses132/booking-api/)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](ramses.booking-api.com)

Booking API project for admission test

## API Booking ADMISSION TEST
First of all this project is just a test for admission using booking api.
I use cookie cutter to get initial code and skip configuration step to default.
to run project you will need use python virtualenv install requirements and requirements.txt and add environment variables in .env file
example .env file

```
SECRET_KEY=examplekey
ALLOWED_HOSTS=127.0.0.1,0.0.0.0,localhost
DEBUG=True
```

if you want use docker and docker compose read installation phase

### Installation

**Requirements**
* docker
* docker-compose

After installing and configuring those, download [docker-compose.yml](https://raw.githubusercontent.com/ramses132/booking-api/master/docker-compose.yml) and run the following command:

```bash
docker-compose up -d
```

You can now access the api at [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/).

### Configuration

Document Merge Service is a [12factor app](https://12factor.net/) which means that configuration is stored in environment variables.
Different environment variable types are explained at [django-environ](https://github.com/joke2k/django-environ#supported-types).

#### ENVIRONMENT

A list of configuration options which you need for use with postgres ()

* `SECRET_KEY`: A secret key used for cryptography. This needs to be a random string of a certain length. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-SECRET_KEY).
* `ALLOWED_HOSTS`: A list of hosts/domains your service will be served from. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts).
* `DATABASE_ENGINE`: Database backend to use. See [more](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-DATABASE-ENGINE). (default: django.db.backends.postgresql)
* `DATABASE_HOST`: Host to use when connecting to database (default: localhost)
* `DATABASE_PORT`: Port to use when connecting to database (default: 5432)
* `DATABASE_NAME`: Name of database to use (default: booking-api)
* `DATABASE_USER`: Username to use when connecting to the database (default: booking-api)
* `DATABASE_PASSWORD`: Password to use when connecting to database


## SWAGGER DOC
we are using `drf-yasg` you can check the endpoint project `/swagger/` to check all the api documentation and test.

### Project endpoints
| name          | endpoint                   | description                                     |
|---------------|----------------------------|-------------------------------------------------|
| create book   | POST: /api/v1/book         | create a new booking                            |
| delete book   | DELETE: /api/v1/book/{id}  | delete booking                                  |
| get events    | GET: /api/v1/events        | get events                                      |
| create events | POST: /api/v1/events       | create new event                                |
| get rooms     | GET: /api/v1/rooms         | get rooms                                       |
| create room   | POST: /api/v1/rooms        | create new room                                 |
| get room      | GET: /api/v1/rooms/{id}    | get room detail                                 |
| patch room    | PATCH: /api/v1/rooms/{id}  | patch room                                      |
| delete room   | DELETE: /api/v1/rooms/{id} | delete room                                     |
| get users     | GET: /api/v1/users         | get all users                                   |
| patch user    | PATCH: /api/v1/users/{id}  | patch user data                                 |
| delete user   | DELETE: /api/v1/users/{id} | delete user                                     |
| login         | POST: /login/              | login using JWT return refresh and access token |
| token refresh | POST: /login/refresh       | refresh access token                            |
| logout        | POST: /logout/             | add refresh token to black list                 |
| register      | POST: /register/           | register new user                               |

## JWT Authentication
we are implementing JWT authentication process you can take access token and refresh token from login endpoint, and with logout endpoint you can set refresh as black list; you need to invalidate token via frontend and manual process.

#

THANKS FOR READ INDENTATION IS LIFE!!