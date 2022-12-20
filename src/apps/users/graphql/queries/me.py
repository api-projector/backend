import graphene
from graphql import GraphQLResolveInfo
from jnt_django_graphene_toolbox.errors import GraphQLPermissionDenied

from apps.users.graphql.types import MeUserType


class MeQueries(graphene.ObjectType):
    """Graphql users queries."""

    me = graphene.Field(MeUserType)

    def resolve_me(self, info: GraphQLResolveInfo):  # noqa: WPS110
        """Resolves current context user."""
        if not info.context.user.is_authenticated:
            return GraphQLPermissionDenied()

        return info.context.user
