#! /bin/bash

set -o errexit

./manage.py migrate

nginx

_UWSGI_OPTS=()
if [ "${UWSGI_PROCESSES_COUNT:-}" != "" ]; then
  _UWSGI_OPTS+=(--processes "${UWSGI_PROCESSES_COUNT}")
fi

uwsgi --ini "docker/server/uwsgi.ini" "${_UWSGI_OPTS[@]}"
