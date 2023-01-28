FROM python:3.10-slim

RUN mkdir /django
WORKDIR /django
EXPOSE 8000

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y python python3-pip python3-dev postgresql-client

COPY restapi/requirements.txt /django/requirements.txt

RUN pip3 install -r requirements.txt

COPY restapi /django

ENTRYPOINT [ "/bin/sh", "/django/entry.sh" ]
CMD [ "RUN" ]
