# LOGS-COLLECTOR

```sh
█░░ █▀█ █▀▀ █▀ ▄▄ █▀▀ █▀█ █░░ █░░ █▀▀ █▀▀ ▀█▀ █▀█ █▀█
█▄▄ █▄█ █▄█ ▄█ ░░ █▄▄ █▄█ █▄▄ █▄▄ ██▄ █▄▄ ░█░ █▄█ █▀▄
```

###  [CHANGELOG.md](CHANGELOG.md)

###  [Russian lang: README.md](README-ru.md)


## Purpose

If you are a developer of software that clients later use in their infrastructure,
you must understand how sometimes it can be difficult to research a problem
with software without access to the server on which this software runs.

To solve this problem, you can configure the software to automatically send 
anonymized crash reports, for example, use Sentry. 
This is not always acceptable to the client; 
Moreover, the information may not be complete or the client 
requires increased confidentiality.


## Terms
- Platform: this is software developed by your company
- Ticket: this is the number associated with the ticket in your help desk system
- Archive: this is an uploaded log file (any format is supported)

## How it works?

- Create platforms
- Create a ticket associated with the platform and number
- Transfer a unique ticket token to the client
- The client downloads an archive of log files
- Download the archive (find a solution to the problem)
- Delete the archive or ticket or mark the ticket as resolved
  
## Features

- Centralized storage;
- To download a file you do not need to provide auth credentials;
- Each download token is unique and associated with only one ticket;
- The token has a limit on the number of attempts and lifetime;
- You can download the file from the console or via the web;
- Fully featured RestFullAPI v1;
- Monitoring free space in storage;
- Deleting an archive or ticket also deletes physical files;
- The application follows the 12 factors application architecture;
- Flexible deployment configuration using environment variables;
- The application is dockerized, the image size is less than 150mb;
- Can work with both sqlite3 and PostgreSQL^15;
- Static management without configuration for this web server;
- healthcheck checking application availability;

## Security

- The download token is not associated with authorization
- The download token has high entropy.
- Two-factor authentication for users
- To download a file - 2FA must be forcibly enabled
- The admin panel has been patched to force the use of 2FA
- The user in the container is not privileged
- Standard Django and DRF protection methods

## Install

### From the docker image:
- Create a directory for the application wherever it is convenient for you
- Create a docker-compose.yml file in the application directory
- Create a .env file in the application directory
- Fill the .env file with the required environment variables, see below

>Example file using docker store and sqlite as default database:

```yaml
version: "3"

# to set environment variables:
# create a .env file in the same directory as docker-compose.yaml

services:
  server:
    image: mois3y/logs_collector:0.1.0
    container_name: logs-collector
    restart: unless-stopped
    env_file:
      - ./.env
    ports:
      - "80:8000"
    volumes:
      - /etc/timezone:/etc/timezone:ro  # optional
      - /etc/localtime:/etc/localtime:ro  # optional
      - logs_collector_data:/data

volumes:
  logs_collector_data:
```

### From the source:
- Clone the repository
- docker-compose.yaml is already in the project directory
- create a .env file in the project root
- fill .env with the required environment variables, see below
- build the image and run the container in the background:
  
```sh
docker-compose up -d --build
```
- You can create your own file and make the necessary edits:
#### docker-compose.yaml PostgreSQL by default:

```yaml
services:
  logs_collector:
    container_name: logs-collector
    build:
      context: .
      args:
        - VERSION=${VERSION}
        - SRC_DIR=${SRC_DIR}
        - SCRIPTS_DIR=${SCRIPTS_DIR}
        - APP_DIR=${APP_DIR}
        - DATA_DIR=${DATA_DIR}
        - WEB_PORT=${WEB_PORT}
        - USER_NAME=${USER_NAME}
        - USER_GROUP=${USER_GROUP}
        - APP_UID=${APP_UID}
        - APP_GID=${APP_GID}
    ports:
      - "${WEB_HOST}:${WEB_PORT}:${WEB_PORT}"
    volumes:
      - type: volume
        source: logs_collector_data
        target: ${APP_DIR}/data
    env_file:
      - ./.env
    depends_on:
      - db
      
  db:
    image: postgres:15-alpine3.18
    container_name: psql-collector
    volumes:
      - logs_collector_psql_data:/var/lib/postgresql/data/
    env_file:
      - ./.env


volumes:
  logs_collector_data:
  logs_collector_psql_data:
```

#### docker-compose-example-psql.yaml c sqlite и bind-mount:

```yaml
version: "3"

# to set environment variables:
# create a .env file in the same directory as docker-compose.yaml

services:
  logs_collector:
    container_name: logs-collector
    build:
      context: .
      args:
        - VERSION=${VERSION}
        - SRC_DIR=${SRC_DIR}
        - SCRIPTS_DIR=${SCRIPTS_DIR}
        - APP_DIR=${APP_DIR}
        - DATA_DIR=${DATA_DIR}
        - WEB_PORT=${WEB_PORT}
        - USER_NAME=${USER_NAME}
        - USER_GROUP=${USER_GROUP}
        - APP_UID=${APP_UID}
        - APP_GID=${APP_GID}
    ports:
      - "${WEB_HOST}:${WEB_PORT}:${WEB_PORT}"
    volumes:
      - "/opt/collector/data:${DATA_DIR}"
      - "/opt/collector/data/db.sqlite3:${DATA_DIR}/db.sqlite3"
    env_file:
      - /.env
```

🔴

❗IMPORTANT❗

If you are using bind-mount and mounting it to your application's storage,
remember user in container is not privileged UID 1000 if mounted file
or the directory will belong to the root
application will not be able to read it and therefore work.

In a production environment, use the application behind your favorite reverse proxy.

Just add it to the docker-compose.yaml stack

>You don't have to do this, but Gunicorn recommends following this rule.
>
>I agree with them, so you have been warned)

🔴

## Environment:
>The application can be configured,
>to do this, pass the following possible variables surroundings.
>If no variable is passed, the default environment variable will be used

```
 █▀▄ ░░█ ▄▀█ █▄░█ █▀▀ █▀█ ▀
 █▄▀ █▄█ █▀█ █░▀█ █▄█ █▄█ ▄
```

| ENV                  | DEFAULT         | INFO                     |
| -------------------- | --------------- | ------------------------ |
| SECRET_KEY           | j9QGbvM9Z4otb47 | ❗change this immediately|
| DEBUG                | False           | use only False in prod   |
| ALLOWED_HOSTS        | '*'             | list separated by commas |
| CSRF_TRUSTED_ORIGINS |                 | list separated by commas |
| DB_URL               |                 | url for connect db       |
| TZ                   | 'UTC'           | server timezone          |



[CSRF_TRUSTED_ORIGINS](https://docs.djangoproject.com/en/4.2/ref/settings/#csrf-trusted-origins)

Required in a Docker environment in a production environment
accepts a list of urls separated by commas
>http://localhost,http://*.domain.com,http://127.0.0.1,http://0.0.0.0


[DB_URL](https://django-environ.readthedocs.io/en/latest/quickstart.html)

Must be specified if you want to use PostgreSQL
This data must match the PostgreSQL container variables

| ENV               | VALUE          |
| ----------------- | -------------- |
| POSTGRES_USER     | admin          |
| POSTGRES_PASSWORD | ddkwndkjdX7RrP |
| POSTGRES_DB       | collector      |

Example:

#### psql://admin:ddkwndkjdX7RrP@psql-collector:5432/collector
- Protocol: **psql://**
- User: **admin**
- Password: **ddkwndkjdX7RrP**
- Address: **psql-collector**
- Port: **5432**
- Database name: **collector**

```
█▀▀ █░█ █▄░█ █ █▀▀ █▀█ █▀█ █▄░█ ▀
█▄█ █▄█ █░▀█ █ █▄▄ █▄█ █▀▄ █░▀█ ▄
```

| ENV                         | DEFAULT        |
| --------------------------- | -------------- |
| GUNICORN_BIND               | '0.0.0.0:8000' |
| GUNICORN_BACKLOG            | 2048           |
| GUNICORN_WORKERS            | 2              |
| GUNICORN_WORKER_CLASS       | 'sync'         |
| GUNICORN_WORKER_CONNECTIONS | 1000           |
| GUNICORN_THREADS            | 1              |
| GUNICORN_TIMEOUT            | 3600           |
| GUNICORN_KEEPALIVE          | 2              |
| GUNICORN_LOGLEVEL           | 'info'         |

[GUNICORN_*](https://docs.gunicorn.org/en/stable/settings.html)

Detailed information about each environment variable is available in
the official documentation.

**GUNICORN_BIND** do not change this since the variable 
is responsible for the listening address and port inside the container.

**GUNICORN_TIMEOUT** is set to 3600 by default.
Such a large timeout is needed to download large files.
Since I tried to make the application minimalistic and not use a task manager,
the file is downloaded in one thread.

If the loading time is more than an hour, the connection will be broken,
this is a feature of the synchronous operation of gunicorn workers;
if you do not have enough time to load, you can increase this value.


❗IMPORTANT❗

Gunicorn is configured to write to the log in the following format:
```python
'%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```
This means that the log will show the IP address of the request only from the header

**X-Forwarded-For**

In a production environment, the application must be behind a reverse proxy


## Helpers
At the root of the project repository there is a scripts directory,
it contains the uploader.sh script with which you can send files
from the console using **curl**.

The syntax is simple:

```cmd
Usage: ./uploader.sh [options [parameters]]

Options:

 -f | --file     full path to upload file required
 -t | --token    access token             required
 -u | --url      target url               required
 -v | --version  print version
 -h | --help     print help
```




## License

GNU GPL 3.0
