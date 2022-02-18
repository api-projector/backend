import pytest

from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project(db):
    """Project."""
    return ProjectFactory.create()
