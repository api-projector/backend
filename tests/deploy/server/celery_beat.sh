#! /bin/bash

celery -A server.celery_app beat \
        -s /var/run/app/celerybeat.schedule \
        --pidfile /var/run/app/celerybeat.pid
