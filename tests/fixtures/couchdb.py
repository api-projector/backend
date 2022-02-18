import pytest

from apps.core import injector as core_injector
from apps.core.logic.interfaces import ICouchDBService
from apps.projects.services import CouchDBCleanupService
from tests.helpers.couchdb import StubCouchDBService


@pytest.fixture()
def couchdb_service():
    """Provides CouchDB mocked service."""
    service = StubCouchDBService()
    core_injector.binder.bind(ICouchDBService, service)

    return service


@pytest.fixture()
def couchdb_cleanup_service(couchdb_service):
    """Provides couchdb service."""
    core_injector.binder.bind(CouchDBCleanupService)

    return core_injector.get(CouchDBCleanupService)
