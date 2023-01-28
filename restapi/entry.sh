#!/bin/sh

echo ">>> Processes are done, Service is ready..."
exec python manage.py runserver 0.0.0.0:8000
