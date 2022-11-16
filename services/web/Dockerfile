FROM python:3.10.1-slim-buster

WORKDIR /code

RUN apt-get update 

RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r  /code/requirements.txt

COPY ./ /code/

ENTRYPOINT ["/code/entrypoint.sh"]