import graphene
from jnt_django_graphene_toolbox.types import BaseModelObjectType

from apps.media.models import Image


class ImageType(BaseModelObjectType):
    """Image graphql type."""

    class Meta:
        model = Image

    url = graphene.String()
