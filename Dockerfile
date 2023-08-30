# app/Dockerfile

# pull the official docker image
FROM python:3.10-alpine as base

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# install dependences
COPY requirements.txt ./
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Now multistage builds
FROM python:3.10-alpine

COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

# set lables about app
LABEL maintainer="s.zhukovskii@ispsystem.com"
LABEL ru.isptech.logs-collector.version=v0.1.0

COPY ./logs_collector /app
WORKDIR /app

COPY entrypoint.sh ./

ENTRYPOINT [ "sh", "entrypoint.sh" ]
