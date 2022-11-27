import pytest
from httpretty import httpretty

from apps.core.logic import messages
from apps.projects.logic.commands.project import import_swagger
from apps.projects.models import SwaggerImport
from apps.projects.models.enums import SwaggerImportState
from tests.helpers.asset_provider import AssetsProvider
from tests.helpers.couchdb import StubCouchDBService
from tests.test_projects.factories import SwaggerImportFactory

_SWAGGER_URL = "http://my.swagger.com/api.json"


@pytest.fixture()
def swagger_import(db) -> SwaggerImport:
    """Create project."""
    return SwaggerImportFactory.create(
        swagger_url=_SWAGGER_URL,
    )


def test_success(
    swagger_import: SwaggerImport,
    couchdb_service: StubCouchDBService,
    assets: AssetsProvider,
) -> None:
    """Test success import from url."""
    httpretty.register_uri(
        httpretty.GET,
        _SWAGGER_URL,
        body=assets.open_file("swagger.json").read(),
    )

    messages.dispatch_message(
        import_swagger.Command(
            swagger_import_id=swagger_import.id,
        ),
    )

    swagger_import.refresh_from_db()

    assert swagger_import.state == SwaggerImportState.DONE
    assert swagger_import.log
