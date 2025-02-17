#!/usr/bin/env bash

# expected to exit on error
set -o errexit

# download all necessary files
pip3 install -r requirements.txt &

# start Django server
python manage.py runserver &

# start celery task worker
celery -A astrics worker --loglevel=info &

# start celery crontab scheduler
celery -A astrics beat -s celerybeat-schedule &

wait
