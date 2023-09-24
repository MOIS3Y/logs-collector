# LOGS-COLLECTOR

```sh
█░░ █▀█ █▀▀ █▀ ▄▄ █▀▀ █▀█ █░░ █░░ █▀▀ █▀▀ ▀█▀ █▀█ █▀█
█▄▄ █▄█ █▄█ ▄█ ░░ █▄▄ █▄█ █▄▄ █▄▄ ██▄ █▄▄ ░█░ █▄█ █▀▄
```
###  [English lang: README.md](README.md)

###  [CHANGELOG.md](CHANGELOG.md)


## Цель

Если вы являетесь разработчиком ПО которое в дальнейшем клиенты используют в своей инфраструктуре, вы должны понимать, как иногда бывает трудно изучить проблему с ПО не имея доступа к серверу на котором это ПО работает.


Для решения этой задачи вы можете настраивать ПО на автоматическую отправку обезличенных отчетов о сбоях например использовать Sentry. Это не всегда приемлемо для клиента, к тому же информация может быть не полной или клиенту требуется повышенная конфиденциальность.


В таком случае вы можете попросить клиента отправить вам нужные лог файлы и изучить их в последствии. Но тут возникает другая проблема вам нужен безопасный способ передачи этих файлов как для вас так и для клиента.
Это мог быть FTP, SFTP, облако etc. Но что если вы не хотите давать клиенту данные для аутентификации и авторизации?

Возможно у вас есть доступ к серверу клиента и вы можете прочитать лог файлы на месте. И казалось бы проблема решена. Но на сервере клиента могут отсутствовать инструменты для удобного изучения лог файлов.
Даже если сотрудник поддержки может забрать себе нужные файлы и изучить их локально, возникает проблема распространения этих файлов между другими сотрудниками.

Logs-collector позволяет решить эти задачи.

Logs-collector является удаленным хранилищем и может принимать и отдавать файлы.


## Термины
- Платформа: это ПО разработанное вашей компанией
- Тикет: это номер связанный с тикетом в вашей help desk системе
- Архив: это загруженный лог файл (поддерживается любой формат)

## Как это работает?

- Создаете платформы
- Создаете тикет связанный с платформой и номером 
- Передаете клиенту уникальный токен тикета
- Клиент загружает архив лог файлов
- Скачиваете архив (находите решение проблемы)
- Удаляете архив или тикет или отмечаете тикет решенным

## Особенности

- Централизованное хранилище
- Для загрузки файла не нужно давать auth credentials
- Каждый токен на загрузку уникален и связан только с одним тикетом
- Токен имеет ограничение на количество попыток и время жизни
- Загрузить файл можно из консоли или через веб
- Полнофункциональный RestFullAPI v1
- Мониторинг свободного пространства в хранилище
- Удаление архива или тикета так же удаляет физические файлы
- Приложение соответствует архитектуре приложения 12 факторов
- Гибкая настройка развертывания переменными окружения
- Приложение докеризировано, размер образа меньше 150mb
- Может работать как с sqlite3 так и с PostgreSQL^15
- Управление статикой без настройки для этого веб сервера
- healthcheck проверка доступности приложения

## Безопасность

- Токен на загрузку не связан с авторизацией
- Токен на загрузку обладает высокой энтропией.
- Двухфакторная аутентификация для пользователей
- Для скачивания файла - 2FA должна быть принудительно включена
- Админ панель пропатчена на принудительное использование 2FA
- Пользователь в контейнере является не привилегированным 
- Стандартные методы защиты Django и DRF

## Установка

### Из docker образа:
- Создайте директорию для приложения где вам удобно
- Создайте файл docker-compose.yml в директории приложения
- Создайте файл .env в директории приложения
- Наполните файл .env требуемыми переменными окружения см. ниже

>Пример файла с использованием хранилища докер и sqlite как база данных по умолчанию:

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

### Из исходников:
- Клонируйте репозиторий
- docker-compose.yaml уже есть в директории с проектом
- создайте в корне проекта файл .env
- наполните .env требуемыми переменными окружения см. ниже
- соберите образ и запустите контейнер в фоне:
  
```sh
docker-compose up -d --build
```
- Вы можете создать свой файл и внести нужные правки:
#### docker-compose-example-psql.yaml c PostgreSQL по умолчанию:

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

❗ВАЖНО❗


Если вы используете bind-mount и монтируете его в хранилище приложения, помните
пользователь в контейнере не привилегирован UID 1000 если примонтированный файл
или директория будет принадлежать root приложение не сможет его прочитать и
следовательно работать.

В продакшн среде используйте приложение за вашим любимым обратным прокси.

Просто добавьте его в стек docker-compose.yaml

>Можно этого не делать, но Gunicorn рекомендуют придерживаться этого правила.
>
>Я солидарен с ними, так что вас предупредили)

🔴

## Переменные окружения:
>Приложение можно настроить, для этого передайте следующие возможные переменные
>окружения.
>Если переменная не передана, будет использоваться переменная окружения по умолчанию

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

Требуется в среде докер в продакшн окружении
принимает список url разделенных запятой
>http://localhost,http://*.domain.com,http://127.0.0.1,http://0.0.0.0


[DB_URL](https://django-environ.readthedocs.io/en/latest/quickstart.html)

Нужно указывать если вы хотите использовать PostgreSQL
Эти данные должны совпадать с переменными контейнера PostgreSQL

| ENV               | VALUE          |
| ----------------- | -------------- |
| POSTGRES_USER     | admin          |
| POSTGRES_PASSWORD | ddkwndkjdX7RrP |
| POSTGRES_DB       | collector      |

Пример:

#### psql://admin:ddkwndkjdX7RrP@psql-collector:5432/collector
- Протокол: **psql://**
- Пользователь: **admin**
- Пароль: **ddkwndkjdX7RrP**
- IP адрес: **psql-collector**
- Порт: **5432**
- Имя БД: **collector**

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

Подробная информация о каждой переменной окружения доступна в официальной документации.

GUNICORN_BIND не изменяйте это так как переменная отвечает за прослушиваемый адрес и порт внутри контейнера.

GUNICORN_TIMEOUT по умолчанию установлена в 3600. Такой большой таймаут нужен для загрузки больших файлов.
Поскольку я старался сделать приложение минималистичным и не использовать менеджер задач загрузка файла идет в один поток.

Если время загрузки будет больше часа соединение разорвется, это особенность синхронной работы воркеров gunicorn если вам не хватает времени на загрузку вы можете увеличить это значение.

❗ВАЖНО❗

Gunicorn настроен писать в лог в следующем формате:
```python
'%({X-Forwarded-For}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
```
Это значит что в логе будет видно IP адрес запроса только из заголовка

**X-Forwarded-For**

В продакшн среде приложение должно быть за обратным прокси


## Помощники
В корне репозитория проекта есть директория scripts в ней лежит скрипт uploader.sh с помощью которого можно отправить файлы из консоли используя curl.

Синтаксис простой:

```cmd
Usage: ./uploader.sh [options [parameters]]

Options:

 -f | --file     full path to upload file required
 -t | --token    access token             required
 -d | --dst      storage domain name      required
 -v | --version  print version
 -h | --help     print help
```


#### Пример:

```sh
./uploader.sh \
    --dst collector.domain.zone \
    --token e63268f4-5946-42eb-a678-b02182f14e87 \
    --file /root/logs/all-logs.tar.gz 
```


## Лицензия

GNU GPL 3.0
