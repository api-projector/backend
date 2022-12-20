import json
from dataclasses import dataclass
from enum import Enum

import injector
import yaml

from apps.core.logic import messages
from apps.core.logic.errors import ObjectNotFoundError
from apps.projects.logic.services.projects.openapi import ProjectOpenApiService
from apps.projects.models import Project


@dataclass(frozen=True)
class QueryResult:
    """Project swagger result."""

    scheme: str


class SchemeFormat(Enum):
    """Supported swagger formats."""

    JSON = "json"  # noqa: WPS115
    YAML = "yaml"  # noqa: WPS115


class Query(messages.BaseQuery[QueryResult]):
    """Project swagger."""

    project: str
    output_format: SchemeFormat = SchemeFormat.JSON


class QueryHandler(messages.BaseQueryHandler[Query]):
    """Provides project swagger."""

    @injector.inject
    def __init__(self, project_swagger_service: ProjectOpenApiService):
        """Initialize."""
        self._project_swagger_service = project_swagger_service

    def handle(self, query: Query) -> QueryResult:
        """Handler."""
        project = self._get_project(query)
        scheme = self._project_swagger_service.get_schema(project)

        return QueryResult(
            scheme=self._format_scheme(scheme, query.output_format),
        )

    def _get_project(self, query: Query) -> Project:
        try:
            return Project.objects.get(id=query.project)
        except Project.DoesNotExist:
            raise ObjectNotFoundError()

    def _format_scheme(
        self,
        scheme: dict,  # type: ignore
        output_format: SchemeFormat,
    ) -> str:
        if output_format == SchemeFormat.JSON:
            return json.dumps(scheme, indent=True)
        elif output_format == SchemeFormat.YAML:
            return yaml.dump(scheme, sort_keys=False)

        return ""
