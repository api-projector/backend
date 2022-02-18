import pytest

from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project(user):
    """Create project."""
    return ProjectFactory.create(owner=user)
