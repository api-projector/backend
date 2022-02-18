from typing import List

import requests
from ibmcloudant.cloudant_v1 import Document

from apps.core.logic.interfaces import ICouchDBService


class StubCouchDBService(ICouchDBService):  # noqa: WPS214
    """Mocked CouchDB service."""

    def __init__(self) -> None:
        """Initializing."""
        self.create_database_called = False
        self.delete_database_called = False
        self.deleted_db_names: List[str] = []
        self._doc_map: dict[str, dict] = {}  # type: ignore

    def set_documents(  # noqa: WPS615
        self,
        docs: dict[str, dict],  # type: ignore
    ):
        """Set documents."""
        self._doc_map = {doc_id: doc for doc_id, doc in docs.items()}

    def list_databases(self):
        """Get all database names."""
        return ["db-1", "db-2", "db-3"]

    def create_database(self, db_name: str):
        """Create database with provided name."""
        self.create_database_called = True

    def delete_database(self, db_name: str) -> None:
        """Delete database with provided name."""
        self.delete_database_called = True
        self.deleted_db_names.append(db_name)

    def get_document(
        self,
        db_name: str,
        doc_id: str,
    ) -> Document:
        """Retrieve document."""
        return self._doc_map.get(doc_id)

    def get_documents(  # noqa: WPS615
        self,
        db_name: str,
        doc_ids: list[str],
    ) -> list[Document]:
        """Retrieve many docs by ids."""
        return [self._doc_map.get(doc_id) for doc_id in doc_ids]

    def post_document(
        self,
        db_name: str,
        document: Document,
    ) -> requests.Response:
        """Post the document to database with provided name."""
