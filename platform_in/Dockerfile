# pull official base image
FROM python:3.8.0-alpine

# set working directory
WORKDIR /project

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY requirements.txt .

RUN apk update  && \
  apk add --no-cache postgresql-libs postgresql-dev ca-certificates gcc musl-dev libressl-dev libc-dev librdkafka librdkafka-dev python-dev netcat-openbsd bash && \
  python3 -m pip install -r requirements.txt --no-cache-dir 

COPY chain.pem .
RUN cat chain.pem >> /usr/local/lib/python3.8/site-packages/certifi/cacert.pem

# add app
COPY . /project/

