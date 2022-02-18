from dataclasses import dataclass

from rest_framework import serializers

from apps.core.utils.objects import Empty, empty
from apps.media.models import Image
from apps.projects.logic.commands.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
)


class ProjectDtoValidator(serializers.Serializer):
    """Create project input."""

    title = serializers.CharField()
    description = serializers.CharField(default="", allow_blank=True)
    figma_integration = FigmaIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )
    emblem = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects,
        required=False,
    )


@dataclass(frozen=True)
class ProjectDto:
    """Create project data."""

    title: str | Empty = empty
    description: str = ""
    figma_integration: str | FigmaIntegrationDto = empty
    emblem: int = empty
