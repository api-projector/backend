import argparse
import json

import yaml
from django.core.management import BaseCommand
from ibmcloudant.cloudant_v1 import Document

from apps.core import injector
from apps.core.logic.interfaces import ICouchDBService
from apps.projects.models import Project


class Command(BaseCommand):
    """Command import open api."""

    def add_arguments(self, parser) -> None:
        """Add arguments."""
        parser.add_argument(
            "--project",
            type=str,
            dest="project_id",
        )
        parser.add_argument(
            "--file",
            type=argparse.FileType("r"),
            dest="source_file",
        )

    def handle(self, *args, **options) -> None:  # noqa: WPS110
        """Command handler."""
        db_name = Project.objects.get(id=options["project_id"]).db_name

        if not db_name:
            self.stdout.write("DB {0} not found".format(db_name))
            return

        couch_db_service = injector.get(ICouchDBService)

        if db_name in couch_db_service.list_databases():
            couch_db_service.delete_database(db_name)
        couch_db_service.create_database(db_name)

        open_api_json = self._get_open_api_json(options)

        spec_doc = Document(
            id="spec",
            model_type="spec",
            paths=self._add_paths(open_api_json, couch_db_service, db_name),
            folders=[],
            scheme={"version": 6},
            schemas=self._add_schemas(
                open_api_json,
                couch_db_service,
                db_name,
            ),
        )

        spec_response = couch_db_service.post_document(
            db_name=db_name,
            document=spec_doc,
        )

        self.stdout.write(
            "Spec: {0}\nImport completed.".format(str(spec_response)),
        )

    def _get_path_docs(self, path, path_meta) -> list[Document]:
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
        open_api_json,
        couch_db_service,
        db_name,
    ) -> list[dict[str, str]]:
        self.stdout.write("Adding paths to db...")
        path_docs = []
        for api_path, api_path_meta in open_api_json["paths"].items():
            for doc_path in self._get_path_docs(api_path, api_path_meta):
                response_add_path = couch_db_service.post_document(
                    db_name=db_name,
                    document=doc_path,
                )
                path_docs.append({"_id": response_add_path["id"]})

        return path_docs

    def _add_schemas(
        self,
        open_api_json,
        couch_db_service,
        db_name,
    ) -> list[dict[str, str]]:
        self.stdout.write("Adding schemas to db...")
        schemas_docs = []
        schemas_items = open_api_json["components"]["schemas"].items()
        for api_schema, api_schema_meta in schemas_items:
            response_add_schema = couch_db_service.post_document(
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

    def _get_open_api_json(self, options) -> dict[str, object]:
        return json.loads(options["source_file"].read())
