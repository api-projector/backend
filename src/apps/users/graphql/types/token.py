import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.users.graphql.types import UserType
from apps.users.models import Token


class TokenType(BaseModelObjectType):
    """Token graphql type."""

    class Meta:
        model = Token

    user = graphene.Field(UserType)
    key = graphene.String()
    created = graphene.DateTime()
