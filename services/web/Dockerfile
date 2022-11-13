# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src/web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/web/requirements.txt
RUN pip install -r requirements.txt

# run entrypoint.sh
ENTRYPOINT ["/usr/src/web/entrypoint.sh"]

# copy app
COPY . /usr/src/web/