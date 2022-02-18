import pytest

from apps.core import injector
from apps.projects.logic.services.projects.openapi import ProjectOpenApiService
from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project(db):
    """Project."""
    return ProjectFactory.create()


@pytest.fixture()
def openapi_service():
    """Openapi service."""
    return injector.get(ProjectOpenApiService)
