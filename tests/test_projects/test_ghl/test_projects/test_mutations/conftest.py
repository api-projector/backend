import pytest

from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture(scope="session")
def create_project_mutation(ghl_mutations):
    """Provides create project graphql mutation."""
    return ghl_mutations.fields["createProject"].resolver


@pytest.fixture(scope="session")
def delete_project_mutation(ghl_mutations):
    """Provides delete project graphql mutation."""
    return ghl_mutations.fields["deleteProject"].resolver


@pytest.fixture(scope="session")
def update_project_mutation(ghl_mutations):
    """Provides update project graphql mutation."""
    return ghl_mutations.fields["updateProject"].resolver


@pytest.fixture()
def project():
    """Provides project."""
    return ProjectFactory.create()
