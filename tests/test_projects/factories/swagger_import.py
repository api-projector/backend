import factory

from apps.projects.models import SwaggerImport
from tests.test_projects.factories.project import ProjectFactory


class SwaggerImportFactory(factory.django.DjangoModelFactory):
    """Swagger import factory."""

    class Meta:
        model = SwaggerImport

    project = factory.SubFactory(ProjectFactory)
