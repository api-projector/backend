import injector

from apps.core.logic.interfaces import ICouchDBService
from apps.projects.models import Project


class CouchDBCleanupService:
    """CouchDB cleanup service."""

    @injector.inject
    def __init__(self, couchdb_service: ICouchDBService):
        """Initialize."""
        self._couchdb_service = couchdb_service

    def cleanup(self):
        """Remove obsolete databases."""
        for_delete = set(self._couchdb_service.list_databases()) - set(
            Project.objects.values_list("db_name", flat=True),
        )

        for delete_db_name in for_delete:
            self._couchdb_service.delete_database(delete_db_name)
