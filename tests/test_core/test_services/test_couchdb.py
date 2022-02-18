from apps.core import injector
from apps.core.logic.interfaces import ICouchDBService
from apps.projects.models import Project
from tests.test_projects.factories.project import ProjectFactory


def test_delete_db(couchdb_service):
    """Test delete db."""
    assert not couchdb_service.delete_database_called

    couch_db = injector.get(ICouchDBService)
    couch_db.delete_database("db_name")

    assert couchdb_service.delete_database_called


def test_cleanup_couch_databases(db, couchdb_service, couchdb_cleanup_service):
    """Test cleanup couchdb."""
    db_names = ("db-1", "db-2")

    assert not couchdb_service.delete_database_called

    for db_name in db_names:
        ProjectFactory.create(db_name=db_name)

    couchdb_cleanup_service.cleanup()

    assert couchdb_service.delete_database_called

    for project in Project.objects.all():
        assert project.db_name not in couchdb_service.deleted_db_names
