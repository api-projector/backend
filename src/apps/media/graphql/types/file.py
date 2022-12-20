import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.media.models import File


class FileType(BaseModelObjectType):
    """File graphql type."""

    class Meta:
        model = File

    url = graphene.String()
