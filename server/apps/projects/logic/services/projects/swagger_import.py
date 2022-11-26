import json

import injector
import yaml
from ibmcloudant.cloudant_v1 import Document

from apps.core.logic import errors
from apps.core.logic.interfaces import ICouchDBService
from apps.projects.models import SwaggerImport

SCHEMA_VER = 6


class SwaggerImportError(errors.BaseApplicationError):
    """Swagger import error."""


class ImportLogger:
    """Swagger import logger."""

    def __init__(self, swagger_import: SwaggerImport):
        """Initialize."""
        self._swagger_import = swagger_import
        self._lines: list[str] = []

    def info(self, log_line: str) -> None:  # noqa: WPS110
        """Info message."""
        self._lines.append(log_line)

    def error(self, log_line: str) -> None:
        """Error message."""
        self._lines.append("ERROR: {0}".format(log_line))

    def flush(self) -> None:
        """Flush log."""
        self._swagger_import.log = "{0}\n{1}".format(
            self._swagger_import.log,
            "\n".join(self._lines),
        )
        self._swagger_import.save(update_fields=["log"])
        self._lines = []


class SwaggerImportService:
    """Generates project swagger."""

    @injector.inject
    def __init__(self, couchdb_service: ICouchDBService):
        """Initialize."""
        self._couchdb_service = couchdb_service

    def import_swagger(
        self,
        swagger_import: SwaggerImport,
        logger: ImportLogger,
    ) -> Document:
        """Import swagger scheme."""
        if not swagger_import.swagger_content:
            logger.error("empty swagger content")
            raise SwaggerImportError()

        scheme_json = json.loads(swagger_import.swagger_content)

        db_name = swagger_import.project.db_name
        if not db_name:
            logger.error("project has no couchdb database")
            raise SwaggerImportError()

        if db_name in self._couchdb_service.list_databases():
            self._couchdb_service.delete_database(db_name)

        self._couchdb_service.create_database(db_name)

        spec_doc = Document(
            id="spec",
            model_type="spec",
            scheme={"version": SCHEMA_VER},
            paths=self._extract_paths(scheme_json, db_name),
            folders=[],
            schemas=self._extract_schemas(scheme_json, db_name),
        )

        self._couchdb_service.post_document(
            db_name=db_name,
            document=spec_doc,
        )

        logger.info("swagger imported")

        return spec_doc

    def _extract_schemas(
        self,
        scheme_json,
        db_name,
    ) -> list[dict[str, str]]:
        schemas_docs = []
        schemas_items = scheme_json["components"]["schemas"].items()
        for api_schema, api_schema_meta in schemas_items:
            response_add_schema = self._couchdb_service.post_document(
                db_name=db_name,
                document=self._get_schema_doc(api_schema, api_schema_meta),
            )
            schemas_docs.append({"_id": response_add_schema["id"]})

        return schemas_docs

    def _get_schema_doc(self, sw_schema, sw_schema_meta) -> Document:
        return Document(
            model_type="schema",
            name=sw_schema,
            json=json.dumps(sw_schema_meta),
            yaml=yaml.dump(sw_schema_meta),
        )

    def _extract_paths(
        self,
        scheme_json,
        db_name: str,
    ) -> list[dict[str, str]]:
        path_docs = []
        for api_path, api_path_meta in scheme_json["paths"].items():
            for path_doc in self._get_path_docs(api_path, api_path_meta):
                response_add_path = self._couchdb_service.post_document(
                    db_name=db_name,
                    document=path_doc,
                )
                path_docs.append({"_id": response_add_path["id"]})

        return path_docs

    def _get_path_docs(self, path: str, path_meta) -> list[Document]:
        documents = []
        allowed_methods = ["get", "post", "patch", "delete", "put"]
        for method_name, method_body in path_meta.items():
            if method_name not in allowed_methods:
                continue
            documents.append(
                Document(
                    model_type="path",
                    method=method_name,
                    url=path[1:],  # path
                    json=json.dumps(method_body),
                    yaml=yaml.dump(method_body),
                    tags=method_body.get("tags", []),
                ),
            )
        return documents
