from dataclasses import dataclass
from typing import Type

from django.db import models
from rest_framework import exceptions

from apps.core.helpers.objects import empty
from apps.core.logic import messages
from apps.core.logic.helpers.validation import validate_input
from apps.projects.logic.commands.project.update import dto
from apps.projects.models import FigmaIntegration, Project
from apps.users.models import User


@dataclass(frozen=True)
class CommandResult:
    """Update project output dto."""

    project: Project


@dataclass(frozen=True)
class Command(messages.BaseCommand[CommandResult]):
    """Update project command."""

    data: dto.ProjectDto  # noqa: WPS110
    project: int
    user: User


class CommandHandler(messages.BaseCommandHandler[Command]):
    """Updating projects."""

    def handle(self, command: Command) -> CommandResult:
        """Main logic here."""
        project = Project.objects.filter(pk=command.project).first()
        if not project:
            raise exceptions.ValidationError("Project not found")

        validated_data = validate_input(
            command.data,
            dto.ProjectDtoValidator,
        )

        self._update_figma_integration(project, validated_data)

        for field, field_value in validated_data.items():
            setattr(project, field, field_value)
        project.save()

        return CommandResult(project=project)

    def _update_figma_integration(
        self,
        project: Project,
        validated_data,
    ) -> None:
        self._update_integration(
            project,
            validated_data,
            FigmaIntegration,
            "figma_integration",
        )

    def _update_integration(
        self,
        project: Project,
        validated_data,
        model: Type[models.Model],
        field: str,
    ):
        integration_dto = validated_data.pop(field, empty)
        if integration_dto != empty:
            if integration_dto:
                model.objects.update_or_create(
                    project=project,
                    defaults={"token": integration_dto["token"]},
                )
            elif integration_dto is None:
                model.objects.filter(project=project).delete()
