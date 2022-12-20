import graphene

from apps.media.graphql.types import FileType
from apps.projects.graphql.types import ProjectType


class ProjectAssetType(graphene.ObjectType):
    """Project asset type."""

    class Meta:
        name = "ProjectAsset"

    project = graphene.Field(ProjectType)
    file = graphene.Field(FileType)  # noqa: WPS110
    source = graphene.String()
    file_url = graphene.String()
