import graphene
from graphene_file_upload.scalars import Upload
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.projects.graphql.mutations.project.inputs import BaseProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.logic.commands.project import create as project_create
from apps.projects.logic.commands.project.create.create import SwaggerSource


class ProjectFromSwaggerType(graphene.InputObjectType):
    """ProjectFromSwagger type."""

    scheme_url = graphene.String()
    scheme = graphene.Field(Upload)


class CreateProjectInput(BaseProjectInput):
    """Input for create project."""

    title = graphene.String(required=True)
    from_swagger = graphene.Field(ProjectFromSwaggerType)


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
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> project_create.Command:
        """Build command."""
        project_data = kwargs.get("input")

        return project_create.Command(
            user=info.context.user,
            data=project_create.ProjectDto(**project_data),
            swagger_source=cls._read_swagger_source(project_data),
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: project_create.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "project": command_result.project,
        }

    @classmethod
    def _read_swagger_source(cls, project_data) -> SwaggerSource | None:
        from_swagger = (
            project_data.pop("from_swagger", None) if project_data else None
        )
        if not from_swagger:
            return None

        scheme_data = from_swagger.get("scheme")
        scheme = None
        if scheme_data:
            scheme = scheme_data.read().decode("utf-8")

        return SwaggerSource(
            scheme_url=from_swagger.get("scheme_url"),
            scheme=scheme,
        )
