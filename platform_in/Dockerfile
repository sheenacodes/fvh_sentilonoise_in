# pull official base image
FROM python:3.8.0-alpine

# set working directory
WORKDIR /project

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# add and install requirements
COPY requirements.txt .

RUN \
 apk update && apk add bash &&\ 
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 apk add --no-cache librdkafka librdkafka-dev && \
 apk add netcat-openbsd &&\
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

 # add entrypoint.sh
#COPY ./entrypoint.sh /project/entrypoint.sh
#RUN chmod +x /project/entrypoint.sh

# add app
COPY . /project/

#ENTRYPOINT ["/project/entrypoint.sh"]
# run server
#CMD python manage.py run -h 0.0.0.0
