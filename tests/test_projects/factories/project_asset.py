import factory

from apps.projects.models import ProjectAsset, ProjectAssetSource
from tests.test_media.factories.file import FileFactory
from tests.test_projects.factories.project import ProjectFactory


class ProjectAssetFactory(factory.django.DjangoModelFactory):
    """Project asset factory."""

    class Meta:
        model = ProjectAsset

    project = factory.SubFactory(ProjectFactory)
    source = ProjectAssetSource.FIGMA
    file = factory.SubFactory(FileFactory)  # noqa: WPS110
