import pytest


@pytest.fixture(scope="session")
def login_mutation(ghl_mutations):
    """
    Login mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["login"].resolve


@pytest.fixture(scope="session")
def logout_mutation(ghl_mutations):
    """
    Logout mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["logout"].resolve


@pytest.fixture(scope="session")
def social_login_complete_mutation(ghl_mutations):
    """
    Social login complete mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["socialLoginComplete"].resolve
