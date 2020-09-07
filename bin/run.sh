#!/bin/bash
set -e

sleep 10

python /etc/sizex/manage.py migrate
python /etc/sizex/manage.py collectstatic --noinput
exec uwsgi --ini /etc/sizex/etc/uwsgi.ini
