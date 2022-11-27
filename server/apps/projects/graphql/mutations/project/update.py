import graphene
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.projects.graphql.mutations.project.inputs import BaseProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.logic.commands.project import update as project_update


class UpdateProjectInput(BaseProjectInput):
    """Input for update project."""


class UpdateProjectMutation(BaseCommandMutation):
    """Update project mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        id = graphene.ID(required=True)  # noqa: WPS125
        input = graphene.Argument(UpdateProjectInput)  # noqa: WPS125

    project = graphene.Field(ProjectType)

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> project_update.Command:
        """Build command."""
        return project_update.Command(
            user=info.context.user,
            project=kwargs["id"],
            data=project_update.ProjectDto(**kwargs.get("input")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: project_update.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "project": command_result.project,
        }
