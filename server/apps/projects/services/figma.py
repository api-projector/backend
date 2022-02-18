import re
from typing import Dict
from urllib.parse import parse_qs, unquote, urlsplit

import requests
from django.utils.translation import gettext_lazy as _

from apps.core.errors import BaseError
from apps.projects.logic.interfaces.figma import (
    IFigmaService,
    IFigmaServiceFactory,
    ImageParams,
)
from apps.projects.models import FigmaIntegration, Project

API_URL_IMAGES = "https://api.figma.com/v1/images/{0}"
RE_FIGMA_URL = r"https://www.figma.com/file/[\w\d_-].+/[\w\d_-].+\?*node-id="


class FigmaError(BaseError):
    """Main figma-exception."""


class IntegrationNotFoundFigmaError(FigmaError):
    """Figma integration not found."""

    code: str = "figma_integration_not_found"
    message = _("MSG__FIGMA_INTEGRATION_NOT_FOUND")


class InvalidUrlFigmaError(FigmaError):
    """Figma integration not found."""

    code: str = "figma_invalid_url"
    message = _("MSG__FIGMA_NOT_VALID_URL")


class ApiFigmaError(FigmaError):
    """Figma api exception."""

    code: str = "figma_api_error"

    def __init__(self, message) -> None:
        """Initialize."""
        self.message = message
        super().__init__()


class FigmaService(IFigmaService):
    """Figma client."""

    def __init__(self, token: str) -> None:
        """Initialize service."""
        self._token = token

    def get_image_url(self, inbound_url) -> str:
        """Get direct url for image."""
        image_params = self.get_image_params(inbound_url)
        figma_api_response = self._get_response(image_params)

        if figma_api_response["err"]:
            msg = _("MSG__FIGMA_REQUEST_ERROR {error}")
            raise ApiFigmaError(msg.format(error=figma_api_response["err"]))

        return figma_api_response["images"][image_params.id]  # type: ignore

    def get_image_params(self, inbound_url: str) -> ImageParams:
        """Get image params."""
        try:
            return self._get_image_params(inbound_url)
        except ValueError:  # noqa: WPS329
            raise InvalidUrlFigmaError()

    def _get_image_params(self, inbound_url: str) -> ImageParams:
        """Parse url-parameters."""
        self._validate_inbound_url(inbound_url)

        decode_url = unquote(inbound_url)
        split_result = urlsplit(decode_url)

        image_key, image_title = split_result.path.split("/")[-2:]
        image_id = parse_qs(split_result.query).get("node-id")[
            0
        ]  # type: ignore

        return ImageParams(image_key, image_title, image_id)

    def _validate_inbound_url(self, inbound_url: str) -> None:
        """
        Validate url by this template.

        Url-template: https://www.figma.com/file/{key}/{title}?node-id={id}
        """
        if not re.match(RE_FIGMA_URL, inbound_url):
            raise ValueError

    def _get_response(self, image_params: ImageParams) -> Dict[str, object]:
        """Get response from figma api."""
        return requests.get(
            API_URL_IMAGES.format(image_params.key),
            params={"ids": image_params.id},
            headers={"X-Figma-Token": self._token},
        ).json()


class FigmaServiceFactory(IFigmaServiceFactory):
    """Figma service factory."""

    def create(self, project: Project) -> FigmaService:
        """Create figma service."""
        try:
            token = project.figma_integration.token
        except FigmaIntegration.DoesNotExist:  # noqa: WPS329
            raise IntegrationNotFoundFigmaError()

        return FigmaService(token)
