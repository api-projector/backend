import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.projects.graphql.mutations.project.inputs import BaseProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.logic.commands.project import create as project_create
from apps.projects.logic.commands.project.create.create import SwaggerSource


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
        root: object | None,
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> project_create.Command:
        """Build command."""
        project_data = kwargs.get("input")

        from_swagger = (
            project_data.pop("from_swagger", None) if project_data else None
        )
        swagger_source = None
        if from_swagger:
            swagger_source = SwaggerSource(
                scheme_url=from_swagger["scheme_url"],
            )

        return project_create.Command(
            user=info.context.user,  # type: ignore
            data=project_create.ProjectDto(**project_data),
            swagger_source=swagger_source,
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: ResolveInfo,  # noqa: WPS110
        command_result: project_create.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "project": command_result.project,
        }
