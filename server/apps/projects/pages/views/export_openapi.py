import types

from django.http import HttpRequest, HttpResponse

from apps.core.logic import messages
from apps.core.pages.base_view import BaseView
from apps.projects.logic.queries import project
from apps.projects.logic.queries.project.openapi import SchemeFormat

CONTENT_TYPE_MAP = types.MappingProxyType(
    {
        SchemeFormat.JSON: "application/json",
        SchemeFormat.YAML: "text/yaml",
    },
)


class View(BaseView):
    """Swagger download view."""

    def get(
        self,
        request: HttpRequest,
        project_id: str,
        output_format: str,
    ) -> HttpResponse:
        """Request handler."""
        scheme_format = SchemeFormat(output_format)
        query_result = messages.dispatch_message(
            project.openapi.Query(
                project=project_id,
                output_format=SchemeFormat(output_format),
            ),
        )

        return HttpResponse(
            query_result.scheme,
            content_type=CONTENT_TYPE_MAP.get(scheme_format),
        )
