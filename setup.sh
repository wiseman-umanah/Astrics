#!/usr/bin/env bash

# expected to exit on error
set -o errexit

# start Django server
gunicorn astrics.wsgi:application --bind 0.0.0.0:8000 &

# start celery task worker
celery -A astrics worker --loglevel=info &

# start celery crontab scheduler
celery -A astrics beat -s celerybeat-schedule &

wait
