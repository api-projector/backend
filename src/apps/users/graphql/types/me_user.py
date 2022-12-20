import graphene

from apps.media.graphql.types import ImageType


class MeUserType(graphene.ObjectType):
    """Me user graphql type."""

    id = graphene.ID()
    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    is_active = graphene.Boolean()
    avatar = graphene.Field(ImageType)
