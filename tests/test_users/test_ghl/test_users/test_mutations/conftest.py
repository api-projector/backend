import pytest


@pytest.fixture(scope="session")
def update_me_mutation(ghl_mutations):
    """
    Update me mutation.

    :param ghl_mutations:
    """
    return ghl_mutations.fields["updateMe"].resolver
