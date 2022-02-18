import pytest


@pytest.fixture(scope="session")
def login_mutation(ghl_mutations):
    """Provides login graphql mutation."""
    return ghl_mutations.fields["login"].resolver


@pytest.fixture(scope="session")
def logout_mutation(ghl_mutations):
    """Provides logout graphql mutation."""
    return ghl_mutations.fields["logout"].resolver


@pytest.fixture(scope="session")
def me_query(ghl_queries):
    """Provides me graphql query."""
    return ghl_queries.fields["me"].resolver


@pytest.fixture(scope="session")
def gl_login_mutation(ghl_mutations):
    """Provides gitlab login graphql mutation."""
    return ghl_mutations.fields["loginGitlab"].resolver


@pytest.fixture(scope="session")
def complete_gl_auth_mutation(ghl_mutations):
    """Provides complete gitlab login graphql mutation."""
    return ghl_mutations.fields["completeGitlabAuth"].resolver
