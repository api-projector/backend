import graphene
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.commands.auth import social_complete_login
from apps.users.logic.interfaces.social_login import SystemBackend


class SocialLoginCompleteMutation(BaseCommandMutation):
    """Complete login mutation after redirection."""

    class Arguments:
        code = graphene.String(required=True)
        state = graphene.String(required=True)
        system = graphene.Argument(
            graphene.Enum.from_enum(SystemBackend),
            required=True,
        )

    token = graphene.Field(TokenType)
    is_new_user = graphene.Boolean()

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> social_complete_login.Command:
        """Create command."""
        return social_complete_login.Command(
            request=info.context,
            code=kwargs["code"],
            state=kwargs["state"],
            system=SystemBackend(kwargs["system"]),
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: social_complete_login.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "token": command_result.token,
            "is_new_user": command_result.is_new_user,
        }
