import pytest


@pytest.fixture(scope="session")
def project_query(ghl_queries):
    """Provides project graphql query."""
    return ghl_queries.fields["project"].resolver


@pytest.fixture(scope="session")
def all_projects_query(ghl_queries):
    """Provides all projects graphql query."""
    return ghl_queries.fields["allProjects"].resolver
