from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.projects.graphql.mutations.project.inputs import BaseProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.logic.commands.project import create as project_create


class CreateProjectInput(BaseProjectInput):
    """Input for create project."""

    title = graphene.String(required=True)


class CreateProjectMutation(BaseCommandMutation):
    """Create project mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(CreateProjectInput)  # noqa: WPS125

    project = graphene.Field(ProjectType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        return project_create.Command(
            user=info.context.user,  # type: ignore
            data=project_create.ProjectDto(**kwargs.get("input")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: project_create.CommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "project": command_result.project,
        }
