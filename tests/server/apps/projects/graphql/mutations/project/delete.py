from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
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
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
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
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "status": "success",
        }
