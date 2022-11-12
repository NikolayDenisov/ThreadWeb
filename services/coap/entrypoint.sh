#!/bin/bash

echo "Waiting for TimescaleDB to be available..."

# Use netcat (nc) to check if the TimescaleDB host/port are accessible
#while ! nc -z timescale 5432; do
#  sleep 0.1
#done

python manage.py
exec "$@"