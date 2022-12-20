import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.media.graphql.types import ImageType
from apps.users.models import User


class UserType(BaseModelObjectType):
    """User graphql type."""

    class Meta:
        model = User

    first_name = graphene.String()
    last_name = graphene.String()
    email = graphene.String()
    is_staff = graphene.Boolean()
    is_active = graphene.Boolean()
    last_login = graphene.DateTime()
    avatar = graphene.Field(ImageType)
