import pytest


@pytest.fixture(scope="session")
def me_query(ghl_queries):
    """Provides me graphql query."""
    return ghl_queries.fields["me"].resolve


@pytest.fixture(scope="session")
def gl_login_mutation(ghl_mutations):
    """Provides gitlab login graphql mutation."""
    return ghl_mutations.login_gitlab.resolver


@pytest.fixture(scope="session")
def complete_gl_auth_mutation(ghl_mutations):
    """Provides complete gitlab login graphql mutation."""
    return ghl_mutations.complete_gitlab_auth.resolver
