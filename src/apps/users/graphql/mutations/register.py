import graphene
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.commands import register


class RegisterInput(graphene.InputObjectType):
    """User register input."""

    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class RegisterMutation(BaseCommandMutation):
    """Register mutation returns."""

    class Arguments:
        input = graphene.Argument(RegisterInput, required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> register.Command:
        """Build command."""
        return register.Command(**kwargs["input"])

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: register.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {
            "token": command_result.token,
        }
