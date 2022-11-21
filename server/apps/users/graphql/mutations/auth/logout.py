import graphene
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.users.logic.commands.auth import logout


class LogoutMutation(BaseCommandMutation):
    """Logout mutation."""

    class Meta:
        auth_required = True

    status = graphene.String()

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> logout.Command:
        """Create command."""
        return logout.Command(
            token=info.context.auth,  # type: ignore
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "status": "success",
        }
