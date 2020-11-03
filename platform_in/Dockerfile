# pull official base image
FROM python:3.8-slim-buster

# set working directory
WORKDIR /project

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

# add app
COPY . /project/

