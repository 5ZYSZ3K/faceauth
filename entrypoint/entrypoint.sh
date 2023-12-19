#!/bin/bash

set -o errexit
set -o nounset

case $1 in
    bootstrap)
        exec /app/entrypoint/bootstrap.sh
        ;;
    start-backend)
        exec /app/entrypoint/start-backend.sh "${@:2}"
        ;;
    *)
        exec "$@"
        ;;
esac
