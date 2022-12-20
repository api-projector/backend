import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")

app = Celery("celery")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update(worker_pool_restarts=True)
app.conf.timezone = "UTC"

app.autodiscover_tasks()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """Add periodic tasks."""
    from apps.projects.tasks import cleanup_couchdb_task  # noqa: WPS433

    sender.add_periodic_task(
        timedelta(hours=1),
        cleanup_couchdb_task.s(),
        name="cleanup projects couchdb",
    )
