# app/Dockerfile

# pull the official docker image
FROM python:3.10-alpine as base

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# install app dependences
COPY requirements.txt ./
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# now multistage builds
FROM python:3.10-alpine

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# default build args
ARG VERSION=0.1.0 \
    APP_DIR=/app \
    DATA_DIR=/app/data \
    SRC_DIR=./logs_collector \
    SCRIPTS_DIR=./scripts \
    WEB_PORT=8000 \
    USER_NAME=collector \
    USER_GROUP=collector \
    APP_UID=1000 \
    APP_GID=1000

# copy app dependences
COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

# add curl and createa user to avoid running container as root &&
# create storage dir
RUN apk add --no-cache --upgrade curl && \
    addgroup --system ${USER_GROUP} --gid ${APP_GID} && \
    adduser --system --uid ${APP_UID} --ingroup ${USER_GROUP} ${USER_NAME} && \
    mkdir -p ${APP_DIR}/data  && \
    chown -R ${USER_NAME}:${USER_GROUP} ${DATA_DIR}

# switch to user
USER ${USER_NAME}

# copy src and entrypoint.sh to app dir
COPY --chown=${USER_NAME}:${USER_GROUP} ${SRC_DIR} ${APP_DIR}
COPY --chown=${USER_NAME}:${USER_GROUP} ${SCRIPTS_DIR}/entrypoint.sh ${APP_DIR}

# set workdir
WORKDIR ${APP_DIR}

# app listens on this port by default
EXPOSE ${WEB_PORT}

# set lables about app
LABEL maintainer="s.zhukovskii@ispsystem.com"
LABEL me.zhukovsky.logs-collector.version=v${VERSION}

# run app
ENTRYPOINT [ "sh", "entrypoint.sh" ]
