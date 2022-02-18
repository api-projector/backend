import typing as ty

import requests
from django.conf import settings
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator
from ibmcloudant import CloudantV1
from ibmcloudant.cloudant_v1 import Document

from apps.core.logic.interfaces import ICouchDBService


class CouchDBService(ICouchDBService):
    """CouchDb client."""

    def __init__(self):
        """Initialize."""
        authenticator = BasicAuthenticator(
            settings.COUCHDB_USER,
            settings.COUCHDB_PASSWORD,
        )

        self._client = CloudantV1(
            authenticator=authenticator,
        )
        self._client.set_service_url(settings.COUCHDB_URL)

    def list_databases(self) -> list[str]:
        """Get all databases."""
        response = self._client.get_all_dbs()
        return ty.cast(list[str], response.get_result())

    def create_database(self, db_name: str):
        """Create database with provided name."""
        self._client.put_database(db_name)

    def delete_database(self, db_name: str) -> None:
        """Create database with provided name."""
        self._client.delete_database(db_name)

    def get_document(self, db_name: str, doc_id: str) -> Document:
        """Retrieve document."""
        return self._client.get_document(
            db=db_name,
            doc_id=doc_id,
        ).get_result()

    def get_documents(
        self,
        db_name: str,
        doc_ids: list[str],
    ) -> list[Document]:
        """Retrieve many docs by ids."""
        response = self._client.post_all_docs(
            db=db_name,
            include_docs=True,
            keys=doc_ids,
        ).get_result()
        return [row["doc"] for row in response["rows"]]

    def post_document(
        self,
        db_name: str,
        document: Document,
    ) -> requests.Response:
        """Post the document to database with provided name."""
        return self._client.post_document(
            db=db_name,
            document=document,
        ).get_result()
