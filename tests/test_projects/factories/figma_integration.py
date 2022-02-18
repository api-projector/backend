import factory

from apps.projects.models import FigmaIntegration
from tests.test_projects.factories.project import ProjectFactory


class FigmaIntegrationFactory(factory.django.DjangoModelFactory):
    """Figma integration factory."""

    class Meta:
        model = FigmaIntegration

    project = factory.SubFactory(ProjectFactory)
    token = factory.Sequence(lambda index: "figma_{0}".format(index))
