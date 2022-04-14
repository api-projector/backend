import json
import typing as ty

import injector
import requests

from apps.core.services import CouchDBService


class CouchDBMaintenanceService:
    """CouchDb client."""

    @injector.inject
    def __init__(self, couchdb_service: CouchDBService):
        """Initialize."""
        self._couchdb_service = couchdb_service

    def cleanup_databases(self, stdout: ty.TextIO | None = None):
        """Cleanup all databases."""
        for db_name in self._couchdb_service.list_databases():
            self._log('cleanup database "{0}"...\n'.format(db_name), stdout)

            db = self._couchdb_service.get_database(db_name)

            self._purge_database(db, stdout)
            self._compact_database(db, stdout)
            self._view_cleanup_database(db, stdout)

        self._couchdb_service.close()

    def _purge_database(
        self,
        db,
        stdout: ty.TextIO | None,
    ):
        self._log("purge... ", stdout)
        response = self._exec_request(db, "_changes", "get")
        counter = 0
        for document in response.json()["results"]:
            if "deleted" in document:
                doc_id = document["id"]
                revisions = [rev["rev"] for rev in document["changes"]]
                self._exec_request(
                    db,
                    "_purge",
                    payload=json.dumps({doc_id: revisions}),
                )

                counter += 1

        self._log("ok, purged {0} docs\n".format(counter), stdout)

    def _compact_database(
        self,
        db,
        stdout: ty.TextIO | None,
    ):
        self._log("compact... ", stdout)
        self._exec_request(db, "_compact")
        self._log("ok\n", stdout)

    def _view_cleanup_database(
        self,
        db,
        stdout: ty.TextIO | None,
    ):
        self._log("view cleanup... ", stdout)
        self._exec_request(db, "_view_cleanup")
        self._log("ok\n", stdout)

    def _exec_request(
        self,
        db,
        action: str,
        method: str = "post",
        payload=None,
    ) -> requests.Response:
        response = db.r_session.request(
            method,
            "{0}/{1}".format(db.database_url, action),
            headers={"Content-Type": "application/json"},
            data=payload,
        )
        response.raise_for_status()
        return response

    def _log(self, text: str, stdout: ty.TextIO | None):
        if not stdout:
            return

        stdout.write(text, ending="")  # type: ignore
