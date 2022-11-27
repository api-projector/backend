import pytest

from apps.core.logic import messages
from apps.projects.logic.commands.project import import_swagger
from apps.projects.models import SwaggerImport
from apps.projects.models.enums import SwaggerImportState
from tests.helpers.asset_provider import AssetsProvider
from tests.helpers.couchdb import StubCouchDBService
from tests.test_projects.factories import SwaggerImportFactory


@pytest.fixture()
def swagger_import(db, assets: AssetsProvider) -> SwaggerImport:
    """Create project."""
    return SwaggerImportFactory.create(
        swagger_content=assets.read("swagger.json"),
    )


def test_success(
    swagger_import: SwaggerImport,
    couchdb_service: StubCouchDBService,
    assets: AssetsProvider,
) -> None:
    """Test success import from content."""
    messages.dispatch_message(
        import_swagger.Command(
            swagger_import_id=swagger_import.id,
        ),
    )

    swagger_import.refresh_from_db()

    assert swagger_import.state == SwaggerImportState.DONE
    assert swagger_import.log
