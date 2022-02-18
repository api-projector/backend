from dataclasses import dataclass

from rest_framework import serializers

from apps.core.utils.objects import Empty, empty
from apps.media.models import Image
from apps.projects.logic.commands.project.dto import (
    FigmaIntegrationDto,
    FigmaIntegrationDtoValidator,
)


@dataclass(frozen=True)
class ProjectMemberDto:
    """Update project member data."""

    user: int
    roles: int


@dataclass(frozen=True)
class ProjectDto:
    """Create project data."""

    title: str | Empty = empty
    description: str = empty
    figma_integration: str | FigmaIntegrationDto = empty
    emblem: int = empty


class ProjectDtoValidator(serializers.Serializer):
    """Update project input."""

    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    figma_integration = FigmaIntegrationDtoValidator(
        allow_null=True,
        required=False,
    )

    emblem = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects,
        required=False,
    )
