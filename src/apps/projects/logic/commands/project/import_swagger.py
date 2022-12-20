from dataclasses import dataclass

import injector

from apps.core.logic import messages
from apps.media.logic.interfaces import IDownloadService
from apps.projects.logic.services.projects.swagger_import import (
    ImportLogger,
    SwaggerImportError,
    SwaggerImportService,
)
from apps.projects.models import SwaggerImport
from apps.projects.models.enums import SwaggerImportState


@dataclass(frozen=True)
class CommandResult:
    """Command result."""


class Command(messages.BaseCommand[CommandResult]):
    """Import swagger command."""

    swagger_import_id: int


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Import swagger."""

    @injector.inject
    def __init__(
        self,
        download_service: IDownloadService,
        swagger_import_service: SwaggerImportService,
    ):
        """Initialize."""
        self._download_service = download_service
        self._swagger_import_service = swagger_import_service

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        swagger_import = SwaggerImport.objects.get(
            id=command.swagger_import_id,
        )
        logger = ImportLogger(swagger_import)

        self._set_import_state(swagger_import, SwaggerImportState.RUNNING)

        try:
            self._import_swagger(swagger_import, logger)
        except SwaggerImportError:
            self._set_import_state(swagger_import, SwaggerImportState.FAILED)
        else:
            self._set_import_state(swagger_import, SwaggerImportState.DONE)

        logger.flush()

        return CommandResult()

    def _import_swagger(
        self,
        swagger_import: SwaggerImport,
        logger: ImportLogger,
    ) -> None:
        logger.info("started")
        logger.flush()

        if not swagger_import.swagger_content:
            self._download_swagger(swagger_import, logger)

        self._swagger_import_service.import_swagger(swagger_import, logger)

    def _download_swagger(
        self,
        swagger_import: SwaggerImport,
        logger: ImportLogger,
    ) -> None:
        if not swagger_import.swagger_url:
            logger.error("empty swagger url")
            raise SwaggerImportError()

        swagger_data = self._download_service.download(
            swagger_import.swagger_url,
        )
        if not swagger_data:
            logger.error("not swagger data")
            raise SwaggerImportError()

        swagger_import.swagger_content = swagger_data.read().decode("utf8")
        swagger_import.save()

        logger.info("downloaded swagger from url")

    def _set_import_state(
        self,
        swagger_import: SwaggerImport,
        state: SwaggerImportState,
    ) -> None:
        swagger_import.state = state
        swagger_import.save(update_fields=["state"])
