import abc
from collections import namedtuple

from apps.projects.models import Project

ImageParams = namedtuple("ImageParams", ("key", "title", "id"))


class IFigmaService(abc.ABC):
    """Figma service interface."""

    @abc.abstractmethod
    def get_image_url(self, inbound_url: str) -> str:
        """Get direct url for image."""

    @abc.abstractmethod
    def get_image_params(self, inbound_url: str) -> ImageParams:
        """Parse url, get image params."""


class IFigmaServiceFactory(abc.ABC):
    """Figma service factory interface."""

    @abc.abstractmethod
    def create(self, project: Project) -> IFigmaService:
        """Create figma service."""
