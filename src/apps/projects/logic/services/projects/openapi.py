import injector
from ibmcloudant.cloudant_v1 import Document

from apps.core.logic.interfaces import ICouchDBService
from apps.projects.models import Project

OPENAPI_VERSION = "3.0.3"


class ProjectOpenApiService:
    """Generates project swagger."""

    @injector.inject
    def __init__(self, couchdb_service: ICouchDBService):
        """Initialize."""
        self._couchdb_service = couchdb_service

    def get_schema(self, project: Project) -> dict:  # type: ignore
        """Get project scheme."""
        spec = self._couchdb_service.get_document(project.db_name, "spec")

        return {
            "openapi": OPENAPI_VERSION,
            "info": {
                "title": project.title,
                "version": "v1",
            },
            "paths": self._get_paths(project, spec),
            "components": {
                "schemas": self._get_schemas(project, spec),
            },
        }

    def _get_paths(
        self,
        project: Project,
        spec: Document,
    ) -> dict:  # type: ignore
        paths: dict = {}  # type: ignore
        spec_paths = spec and spec.get("paths")
        if not spec_paths:
            return paths

        for path_doc in self._get_path_docs(project, spec_paths):
            url = "/{0}".format(path_doc["url"])
            if url not in paths:
                paths[url] = {}

            paths[url][path_doc["method"]] = path_doc["json"]

        return paths

    def _get_path_docs(self, project: Project, spec_paths):
        return self._couchdb_service.get_documents(
            project.db_name,
            [spec_path["_id"] for spec_path in spec_paths],
        )

    def _get_schemas(
        self,
        project: Project,
        spec: Document,
    ) -> dict:  # type: ignore
        schemas: dict = {}  # type: ignore
        if not spec:
            return schemas

        spec_schemas = spec.get("schemas")
        if not spec_schemas:
            return schemas

        schema_docs = self._couchdb_service.get_documents(
            project.db_name,
            [spec_path["_id"] for spec_path in spec_schemas],
        )

        return {
            schema_doc["name"]: schema_doc["json"]
            for schema_doc in schema_docs
        }
