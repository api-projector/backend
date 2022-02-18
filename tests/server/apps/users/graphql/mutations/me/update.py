from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
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
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Create command."""
        return update.Command(
            user=info.context.user,  # type: ignore
            **kwargs["input"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: update.CommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"me": command_result.user}
