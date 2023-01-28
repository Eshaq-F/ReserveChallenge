#!/bin/sh

set -e

cmd=$1

if [ $cmd = 'RUN' ]; then
  python manage.py migrate
  python manage.py seed
  exec python manage.py runserver 0.0.0.0:8000
fi
