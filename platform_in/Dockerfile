# pull official base image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /project

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## install nc
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd

# add and install requirements
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt
#apt-get update  && \

COPY . /project/


