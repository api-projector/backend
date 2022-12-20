from graphql import GraphQLResolveInfo
from jnt_django_graphene_toolbox.errors import (
    GraphQLInputError,
    GraphQLPermissionDenied,
)
from jnt_django_graphene_toolbox.mutations import BaseMutation

from apps.core.graphql.errors import GenericGraphQLError
from apps.core.logic.errors import (
    AccessDeniedApplicationError,
    BaseApplicationError,
    InvalidInputApplicationError,
)
from apps.core.tasks import messages


class BaseCommandMutation(BaseMutation):
    """Base class for mutations based on command."""

    class Meta:
        abstract = True

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Overrideable mutation operation."""
        try:
            command_result = messages.dispatch_message(
                cls.build_command(root, info, **kwargs),
            )
        except InvalidInputApplicationError as err:
            return GraphQLInputError(err.errors)
        except AccessDeniedApplicationError:
            return GraphQLPermissionDenied()
        except BaseApplicationError as err:
            return GenericGraphQLError(err)

        return cls(**cls.get_response_data(root, info, command_result))

    @classmethod
    def build_command(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        validated_data,
    ):
        """Stub for getting command."""
        raise NotImplementedError()

    @classmethod
    def get_response_data(
        cls,
        root: object | None,
        info: GraphQLResolveInfo,  # noqa: WPS110
        command_result,
    ) -> dict[str, object]:
        """Stub for getting usecase input dto."""
        return {}
