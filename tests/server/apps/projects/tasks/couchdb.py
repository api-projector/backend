from apps.core import injector
from apps.projects.services import CouchDBCleanupService
from celery_app import app


@app.task
def cleanup_couchdb_task() -> None:
    """Cleanup couchdb task."""
    injector.get(CouchDBCleanupService).cleanup()
