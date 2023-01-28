#!/bin/sh

set -e

var=$1

if [ $var = "RUN" ]; then
    python manage.py migrate
    python manage.py seed
    exec python manage.py runserver 0.0.0.0:8000
fi
