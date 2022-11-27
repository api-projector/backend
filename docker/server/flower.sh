#! /bin/bash

set -o errexit

celery -A server.celery_app flower --url_prefix=admin/flower
