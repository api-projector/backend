import json
from typing import Dict, Optional

from graphene_django.views import GraphQLView
from graphene_file_upload.utils import place_files_in_operations
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request

from apps.core.graphql.security.authentication import TokenAuthentication


class ApiGraphQLView(GraphQLView):
    """Api GraphQL View."""

    @classmethod
    def as_view(cls, *args, **kwargs):
        """Main entry point for a request-response process."""
        view = super().as_view(*args, **kwargs)
        view = permission_classes((AllowAny,))(view)
        view = authentication_classes([TokenAuthentication])(view)
        view = api_view(["GET", "POST"])(view)

        return view  # noqa: WPS331

    def parse_body(self, request):
        """Parse body."""
        parsed_data = self._parse_multipart(request)
        if parsed_data:
            return parsed_data
        elif isinstance(request, Request):
            return request.data

        return super().parse_body(request)

    def _parse_multipart(self, request) -> Optional[Dict[str, object]]:
        """Handle multipart request spec for multipart/form-data."""
        content_type = self.get_content_type(request)
        if content_type == "multipart/form-data":
            operations = json.loads(
                request.POST.get("operations", "{}"),  # noqa: P103
            )
            files_map = json.loads(request.POST.get("map", "{}"))  # noqa: P103
            return place_files_in_operations(
                operations,
                files_map,
                request.FILES,
            )
        return None
