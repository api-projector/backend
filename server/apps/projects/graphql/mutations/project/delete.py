import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.projects.logic.commands.project import delete as project_delete


class DeleteProjectMutation(BaseCommandMutation):
    """Delete project mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        project = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> project_delete.Command:
        """Build command."""
        return project_delete.Command(
            user=info.context.user,  # type: ignore
            data=project_delete.ProjectDeleteData(
                project=kwargs["project"],
            ),
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: ResolveInfo,  # noqa: WPS110
        command_result,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "status": "success",
        }
