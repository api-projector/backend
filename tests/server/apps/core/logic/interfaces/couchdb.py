import abc

import requests
from ibmcloudant.cloudant_v1 import Document


class ICouchDBService(abc.ABC):
    """CouchDb service interface."""

    @abc.abstractmethod
    def list_databases(self) -> list[str]:
        """Get all databases."""

    @abc.abstractmethod
    def create_database(self, db_name: str):
        """Create database with provided name."""

    @abc.abstractmethod
    def delete_database(self, db_name: str) -> None:
        """Delete database with provided name."""

    @abc.abstractmethod
    def get_document(self, db_name: str, doc_id: str) -> Document:
        """Retrieve document."""

    @abc.abstractmethod
    def get_documents(
        self,
        db_name: str,
        doc_ids: list[str],
    ) -> list[Document]:
        """Retrieve many docs by ids."""

    @abc.abstractmethod
    def post_document(
        self,
        db_name: str,
        document: Document,
    ) -> requests.Response:
        """Post the document to database with provided name."""
