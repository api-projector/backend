import json

import injector
import yaml
from ibmcloudant.cloudant_v1 import Document

from apps.core.logic.interfaces import ICouchDBService
from apps.projects.models import Project


class SwaggerImportService:
    """Generates project swagger."""

    @injector.inject
    def __init__(self, couchdb_service: ICouchDBService):
        """Initialize."""
        self._couchdb_service = couchdb_service

    def import_scheme(self, project: Project, scheme: str) -> None:
        """Import swagger scheme."""
        db_name = project.db_name

        if not db_name:
            return

        if db_name in self._couchdb_service.list_databases():
            self._couchdb_service.delete_database(db_name)
        self._couchdb_service.create_database(db_name)

        scheme_json = json.loads(scheme)

        spec_doc = Document(
            id="spec",
            model_type="spec",
            paths=self._add_paths(scheme_json, db_name),
            folders=[],
            scheme={"version": 6},
            schemas=self._add_schemas(
                scheme_json,
                db_name,
            ),
        )

        self._couchdb_service.post_document(
            db_name=db_name,
            document=spec_doc,
        )

    def _get_path_docs(self, path: str, path_meta) -> list[Document]:
        documents = []
        allowed_methods = ["get", "post", "patch", "delete", "put"]
        for method_name, method_body in path_meta.items():
            if method_name not in allowed_methods:
                continue
            documents.append(
                Document(
                    method=method_name,
                    url=path[1:],  # path
                    json=json.dumps(method_body),
                    yaml=yaml.dump(method_body),
                    model_type="path",
                    tags=method_body.get("tags", []),
                ),
            )
        return documents

    def _add_paths(
        self,
        scheme_json,
        db_name: str,
    ) -> list[dict[str, str]]:
        path_docs = []
        for api_path, api_path_meta in scheme_json["paths"].items():
            for doc_path in self._get_path_docs(api_path, api_path_meta):
                response_add_path = self._couchdb_service.post_document(
                    db_name=db_name,
                    document=doc_path,
                )
                path_docs.append({"_id": response_add_path["id"]})

        return path_docs

    def _add_schemas(
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

    def _get_scheme_json(self, options) -> dict[str, object]:
        return json.loads(options["source_file"].read())
