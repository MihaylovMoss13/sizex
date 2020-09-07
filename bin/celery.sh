#! /bin/bash
set -e

export C_FORCE_ROOT=1
cd /etc/sizex/
exec celery -A sizex worker -BE --loglevel=INFO -Ofair --maxtasksperchild=100
