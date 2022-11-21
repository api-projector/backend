import graphene
from graphql import GraphQLResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.users.graphql.types import UserType
from apps.users.logic.commands.me import update


class UpdateMeInput(graphene.InputObjectType):
    """User update input."""

    first_name = graphene.String()
    last_name = graphene.String()


class UpdateMeMutation(BaseCommandMutation):
    """Register mutation returns user as me."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(UpdateMeInput, required=True)

    me = graphene.Field(UserType)

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> update.Command:
        """Create command."""
        return update.Command(
            user=info.context.user,
            **kwargs["input"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result: update.CommandResult,
    ) -> dict[str, object]:
        """Prepare response data."""
        return {"me": command_result.user}
