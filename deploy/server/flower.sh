#! /bin/bash

set -o errexit

_CELERY_OPTS="-A server.celery_app flower --url_prefix=admin/flower"
if [ "${FLOWER_USER:-}" != "" ] && [ "${FLOWER_PASSWORD:-}" != "" ]
then
  _CELERY_OPTS="${_CELERY_OPTS} --basic_auth=${FLOWER_USER}:${FLOWER_PASSWORD}"
fi

celery ${_CELERY_OPTS}

