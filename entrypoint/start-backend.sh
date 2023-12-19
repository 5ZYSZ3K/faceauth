#!/bin/sh

set -o errexit
set -o nounset

./entrypoint/wait-for-it.sh db:5432 -- echo "Database is up"

python manage.py runserver 0.0.0.0:8000 "$@"
