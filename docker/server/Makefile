CPU_COUNT = $(shell nproc)

UWSGI_PROCESSES_COUNT ?= ${CPU_COUNT}
CELERY_CONCURRENCY ?= ${CPU_COUNT}

.PHONY: server
server:
	@python server/manage.py migrate
	@nginx
	@uwsgi --ini uwsgi.ini --processes ${UWSGI_PROCESSES_COUNT}

.PHONY: celery-beat
celery-beat:
	@rm -f /var/run/app/celerybeat.pid
	@celery -A server.celery_app beat \
        -s /var/run/app/celerybeat.schedule \
        --pidfile /var/run/app/celerybeat.pid

.PHONY: celery-worker
celery-worker:
	@celery -A server.celery_app worker --concurrency ${CELERY_CONCURRENCY}

.PHONY: flower
flower:
	@celery -A server.celery_app flower --url_prefix=admin/flower
